"""
These tests take way longer to complete and are for that reason separated.
"""

import os

from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.models import Page, Overlay, LayoutAnalysisModel
from documents.ocr_engines import init_engines
from scheduler.ocr_tasks import ocr_page

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
FILENAME_IMAGE = os.path.join(ROOT, "backend/tests/examples_data/19154766-page0.jpg")
FILENAME_XML = os.path.join(ROOT, "backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml")

NL = "NL"
FR = "FR"


class OcrPageTest(TransactionTestCase):
    def setUp(self) -> None:
        create()

        self.page = Page.objects.all()[0]

        init_engines()
        self.printed_engine = LayoutAnalysisModel.objects.filter(name__icontains='printed')[0]

    def test_pipeline(self):
        overlays_before = list(Overlay.objects.all())

        ocr_page(self.page.pk,
                 engine_pk=self.printed_engine.pk
                 )

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

        overlays0 = list(Overlay.objects.all())

        for engine in LayoutAnalysisModel.objects.all():
            name = engine.name
            with self.subTest(f"engine {name}"):

                ocr_page(self.page.pk,
                         engine_pk=engine.pk)

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
