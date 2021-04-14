from django.test import TestCase

# The following import gives an error:
# from backend.documents.models import Document
from documents.models import Document, Image


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

        Image.objects.create(
            filename=self.name,
            path=self.path,
            width=self.width,
            height=self.height,
            document=self.doc
        )

    def test_image_content(self):
        image_test = Image.objects.get(filename=self.name)

        self.assertEqual(image_test.path, self.path)

    def test_string_representation(self):
        image_test = Image.objects.get(filename=self.name)

        self.assertEqual(str(image_test), self.name)
