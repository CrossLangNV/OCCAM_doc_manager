import unittest

from documents.metadata import Metadata


# from django.test import TransactionTestCase
#
# from backend.tests.documents.create_database_mock import create
# from documents.models import Page, Overlay
# from scheduler.ocr_tasks import xml_lang_detect, ocr_page

# ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
# FILENAME_IMAGE = os.path.join(ROOT, 'backend/tests/examples_data/19154766-page0.jpg')
# FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')
#
#
# class MetadataTest(TransactionTestCase):
#
#     def setUp(self) -> None:
#         create()
#
#     def test_init(self):
#         overlays0 = list(Overlay.objects.all())
#         page = Page.objects.all()[0]
#
#         metadata = Metadata.from_page(page)


class MetadataTest2(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_init(self):
        metadata = Metadata(titles='name',
                            languages='NL')

        self.assertTrue(metadata)

        xml = metadata.to_xml()

        self.assertTrue(xml)
