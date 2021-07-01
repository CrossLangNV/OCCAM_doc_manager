import io
import logging
import os
import signal

from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.models import Page, Overlay, LayoutAnalysisModel
from documents.ocr_connector import get_engines
from documents.ocr_engines import init_engines
from scheduler.ocr_tasks import xml_lang_detect, ocr_page

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FILENAME_IMAGE = os.path.join(ROOT, "backend/tests/examples_data/19154766-page0.jpg")
FILENAME_XML = os.path.join(ROOT, "backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml")

NL = "NL"
FR = "FR"

B_DEBUG = False


class XMLLangDetectTest(TransactionTestCase):
    def test_lang_detect_filename(self):
        lang = xml_lang_detect(FILENAME_XML)

        self.assertEqual(lang, NL, "Should detect Dutch language")

    def test_lang_detect_string(self):
        with open(FILENAME_XML, "rb") as f:
            s = f.read()

        with io.BytesIO(s) as f:
            lang = xml_lang_detect(f)

        self.assertEqual(lang, NL, "Should detect Dutch language")


class OcrPageTest(TransactionTestCase):
    def setUp(self) -> None:
        create()

        self.page = Page.objects.all()[0]

        init_engines()

    def test_call(self):
        overlays_before = list(Overlay.objects.all())

        ocr_page(self.page.pk)

        overlays_new = list(filter(lambda overlay_i: overlay_i not in overlays_before, Overlay.objects.all()))

        with self.subTest("Sanity check: Should only return one value"):
            self.assertTrue(len(overlays_new), 1)

        overlay_new = overlays_new[0]
        self.assertEqual(overlay_new.source_lang, FR)

    def test_engine_id(self):
        """
        Compare the different results with selecting different engines

        Returns:
            None
        """

        engines = get_engines()

        overlays0 = list(Overlay.objects.all())

        for name, info in engines.items():
            with self.subTest(f"engine {name}"):
                engine_id = info["id"]

                ocr_page(self.page.pk, engine_pk=engine_id)

                # TODO check if this is a good way to evaluate:
                overlays1 = list(filter(lambda overlay_i: overlay_i not in overlays0, Overlay.objects.all()))

                with self.subTest("Sanity check: Should only return one value"):
                    self.assertTrue(len(overlays1), 1)

                overlay_new = overlays1[0]

                if B_DEBUG:
                    filebase, ext = os.path.splitext(overlay_new.file.name)
                    filename_local = os.path.join(
                        os.path.dirname(__file__), f'overlay_engine_{"_".join(name.split(" "))}.xml'
                    )

                    with open(filename_local, "wb") as f_local:
                        with overlay_new.file.open("rb") as f_overlay:
                            f_local.write(f_overlay.read())

                self.assertEqual(overlay_new.source_lang, FR)

    def test_engine_object(self):

        # make sure it's on a reasonable value.
        @break_after(15)
        def test_ocr_page(*args, **kwargs):
            return ocr_page(*args, **kwargs)

        for engine in LayoutAnalysisModel.objects.all():

            with self.subTest(f'Engine {engine.name}'):

                log_stream = io.StringIO()
                logging.basicConfig(stream=log_stream, level=logging.INFO)

                try:
                    test_ocr_page(page_id=self.page.pk,
                                  engine_pk=engine.pk)
                except TimeoutException:
                    # Expected behaviour

                    ocr_engine_message = "Sent request to per ocr:"

                    log_messages = log_stream.getvalue()
                    # print(log_messages)
                    self.assertIn(ocr_engine_message, log_messages,
                                  "Couldn't find a message that indicates that a request for OCR is send.\n"
                                  "Make Sure that 1) this info is logged and "
                                  "2) that call is given enough time to get there.")
                except Exception:
                    self.fail("This didn't work as intended.")

                else:
                    # Weirdly enough this should have stopped before it was done.
                    pass

    def test_engine_object_fail(self):
        """
        Tests unexpected behaviour and how it should be handled.

        Returns:

        """

        NO_ENGINE_PK = -1337
        self.assertFalse(LayoutAnalysisModel.objects.filter(pk=NO_ENGINE_PK),
                         "Sanity check, there should be no object with this id")

        try:
            ocr_page(self.page.pk, engine_pk=NO_ENGINE_PK)
        except Exception as e:
            self.assertIn(str(NO_ENGINE_PK), str(e.args[0]),
                          "Exception should mention that the engine could not be found."
                          )
        else:
            self.fail('"{0}" was expected to throw "{1}" exception'
                      .format(ocr_page.__name__, Exception.__name__))

    def assertRaisesWithMessage(self, exception_type, message, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception_type as e:
            self.assertEqual(e.args[0], message)
        else:
            self.fail('"{0}" was expected to throw "{1}" exception'
                      .format(func.__name__, exception_type.__name__))


class TimeoutException(Exception):
    """
    Custom exception class
    """
    pass


def break_after(seconds=10):
    def timeout_handler(signum, frame):  # Custom signal handler
        raise TimeoutException

    def function(function):
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            try:
                res = function(*args, **kwargs)
                signal.alarm(0)  # Clear alarm
                return res
            except TimeoutException as e:
                print(u'Oops, timeout: %s sec reached.' % seconds, function.__name__, args, kwargs)
                raise e

        return wrapper

    return function
