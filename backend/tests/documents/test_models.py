import os

from django.db.models import FileField
from django.test import TestCase

# The following import gives an error:
# from backend.documents.models import Document
from documents.models import Document, Page, Overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))


class DocumentTest(TestCase):
    """
    Test module for Document model
    """

    def setUp(self):
        """
        Builds up a test database and is cleaned after each test.
        """
        self.name = 'Declaration of Independence'
        self.content = 'Stolen by Nicolas Cage.'

        Document.objects.create(
            name=self.name,
            content=self.content
        )

    def test_document_content(self):
        doc_independence = Document.objects.get(name=self.name)

        self.assertEqual(doc_independence.content, self.content)

    def test_string_representation(self):
        doc_independence = Document.objects.get(name=self.name)

        self.assertEqual(str(doc_independence), self.name)


class ImageTest(TestCase):
    """
    Test module for Image model
    """

    def setUp(self):
        """
        Builds up a test database and is cleaned after each test.
        """

        self.doc = Document.objects.create(
            name='Declaration of Independence',
            content='Stolen by Nicolas Cage.'
        )
        self.name = 'a test image'
        self.path = 'a/b/c.def'
        self.width = 10
        self.height = 20

        Page.objects.create(
            filename=self.name,
            path=self.path,
            width=self.width,
            height=self.height,
            document=self.doc
        )

    def test_image_content(self):
        image_test = Page.objects.get(filename=self.name)

        self.assertEqual(image_test.path, self.path)

    def test_string_representation(self):
        image_test = Page.objects.get(filename=self.name)

        self.assertEqual(str(image_test), self.name)


class OverlayTest(TestCase):
    """
    Test module for Overlay model
    """

    def setUp(self):
        """
        Builds up a test database and is cleaned after each test.
        """

        self.doc = Document.objects.create(
            name='test doc',
            content='test content.'
        )

        self.page = Page.objects.create(
            filename='image.jpg',
            path='images/image.jpg',
            width=10,
            height=20,
            document=self.doc
        )

        self.overlay = Overlay.objects.create(
            page=self.page
        )

    def test_overlay_content(self):
        overlay_test = Overlay.objects.get(page=self.page)

        self.assertEqual(overlay_test.id, self.overlay.id)

    def test_string_representation(self):
        overlay_test = Overlay.objects.get(page=self.page)

        self.assertIn(self.page.filename, str(overlay_test))

    def test_load_xml(self):
        self.assertFalse(self.overlay.xml, 'Sanity check, start with no xml.')

        filename_xml = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')

        with open(filename_xml, 'r') as f:
            self.overlay.update_xml(f)

        self.assertTrue(self.overlay.xml, 'Overlay should contain an XML.')

        self.assertIsInstance(self.overlay.xml, FileField)
