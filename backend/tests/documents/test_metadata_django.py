from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.metadata_django import MetadataDjango
from documents.models import Page, Overlay
from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.metadata_django import MetadataDjango
from documents.models import Page, Overlay


class MetadataTest(TransactionTestCase):

    def setUp(self) -> None:
        create()

    def test_init(self):
        overlays0 = list(Overlay.objects.all())
        page = Page.objects.all()[0]

        metadata = MetadataDjango.from_page(page)

        self.assertTrue(metadata)

        self.assertTrue(metadata.to_xml())
