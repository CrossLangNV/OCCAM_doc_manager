import io
import os

from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.models import Page, Overlay
from documents.ocr_connector import get_engines
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

    def test_call(self):
        overlays0 = list(Overlay.objects.all())
        page = Page.objects.all()[0]

        ocr_page(page.pk)

        overlays1 = list(filter(lambda overlay_i: overlay_i not in overlays0, Overlay.objects.all()))

        with self.subTest("Sanity check: Should only return one value"):
            self.assertTrue(len(overlays1), 1)

        overlay_new = overlays1[0]
        self.assertEqual(overlay_new.source_lang, FR)

    def test_engine_id(self):
        """
        Compare the different results with selecting different engines

        Returns:
            None
        """

        engines = get_engines()

        overlays0 = list(Overlay.objects.all())
        page = Page.objects.all()[0]

        for name, info in engines.items():
            with self.subTest(f"engine {name}"):
                engine_id = info["id"]

                ocr_page(page.pk, engine_id=engine_id)

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
