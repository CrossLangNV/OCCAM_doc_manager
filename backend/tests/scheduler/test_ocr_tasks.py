import io
import logging
import os
import signal

from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.fixtures.engines_main import ENGINES_JSON
from documents.models import Page, LayoutAnalysisModel
from scheduler.ocr_tasks import xml_lang_detect, ocr_page_pipeline

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FILENAME_IMAGE = os.path.join(ROOT, "backend/tests/examples_data/19154766-page0.jpg")
FILENAME_XML = os.path.join(ROOT, "backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml")

NL = "NL"
FR = "FR"

B_DEBUG = False

LOG_STREAM = io.StringIO()
logging.basicConfig(stream=LOG_STREAM, level=logging.INFO)


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
    fixtures = [ENGINES_JSON]

    def setUp(self) -> None:
        create()

        self.page = Page.objects.all()[0]

        # init_engines()
        self.printed_engine = LayoutAnalysisModel.objects.filter(name__icontains='printed')[0]

    def test_engine_object(self):

        # make sure it's on a reasonable value.
        @break_after(10)
        def test_ocr_page(*args, **kwargs):
            return ocr_page_pipeline(*args, **kwargs)

        def truncate(sio: io.StringIO):
            """
            Clears the stringIO

            Args:
                sio:

            Returns:

            """
            sio.truncate(0)
            sio.seek(0)
            return sio

        for engine in LayoutAnalysisModel.objects.all():

            with self.subTest(f'Engine {engine.name}'):

                truncate(LOG_STREAM)

                try:
                    test_ocr_page(page_pk=self.page.pk,
                                  engine_pk=engine.pk)
                except TimeoutException:
                    # Expected behaviour

                    ocr_engine_message = "Sent request to pero ocr:".lower()

                    log_messages = LOG_STREAM.getvalue().lower()
                    # print(log_messages)
                    self.assertIn(ocr_engine_message, log_messages,
                                  "Couldn't find a message that indicates that a request for OCR is send.\n"
                                  "Make Sure that 1) this info is logged and "
                                  "2) that call is given enough time to get there.")

                    self.assertIn(engine.name.lower(), log_messages,
                                  "Couldn't find mention of this engine.")

                except Exception as e:
                    self.fail("Method shouldn't raise any errors.\n{e}")

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
            ocr_page_pipeline(page_pk=self.page.pk, engine_pk=NO_ENGINE_PK)
        except Exception as e:

            # self.assertIn(str(NO_ENGINE_PK), str(e.args[0]),
            #               "Exception should mention that the engine could not be found."
            #               )
            self.assertIn(LayoutAnalysisModel.__name__, str(e.args[0]),
                          "Exception should mention that the engine could not be found."
                          )

        else:
            self.fail('"{0}" was expected to throw "{1}" exception'
                      .format(ocr_page_pipeline.__name__, Exception.__name__))


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
                print(u'Timeout: %s sec reached.' % seconds, function.__name__, args, kwargs)
                raise e

        return wrapper

    return function
