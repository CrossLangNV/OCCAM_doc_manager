import os

from django.db.utils import IntegrityError
from django.test import TransactionTestCase

# The following import gives an error:
# from backend.documents.models import Document
from documents.models import Document, Page, Overlay, Geojson

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FILENAME_IMAGE = os.path.join(ROOT, 'backend/tests/examples_data/19154766-page0.jpg')
FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')


class DocumentTest(TransactionTestCase):
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


class ImageTest(TransactionTestCase):
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
        self.path = 'a/b/c.def'
        self.width = 10
        self.height = 20

        Page.objects.create(
            width=self.width,
            height=self.height,
            document=self.doc
        )

    def test_image_content(self):
        image_test = Page.objects.get(document=self.doc)

        self.assertTrue(image_test, 'Should return an object.')
        self.assertIsInstance(image_test, Page)

    def test_string_representation(self):
        image_test = Page.objects.get(document=self.doc)

        with open(FILENAME_IMAGE, 'rb') as f:
            image_test.update_image(f)

        basename = os.path.split(os.path.splitext(FILENAME_IMAGE)[0])[-1]

        self.assertIn(basename, str(image_test))


class OverlayTest(TransactionTestCase):
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
            # filename='image.jpg',
            # path='images/image.jpg',
            width=10,
            height=20,
            document=self.doc
        )
        with open(FILENAME_IMAGE, 'rb') as f:
            self.page.update_image(f)

        self.overlay = Overlay.objects.create(
            page=self.page
        )

    def test_overlay_content(self):
        overlay_test = Overlay.objects.get(page=self.page)

        self.assertEqual(overlay_test.id, self.overlay.id)

    def test_string_representation(self):
        overlay_test = Overlay.objects.get(page=self.page)

        self.assertIn(self.page.file.name, str(overlay_test))

    def test_load_xml(self):
        self.assertFalse(self.overlay.file, 'Sanity check, start with no xml.')

        with open(FILENAME_XML, 'rb') as f:
            self.overlay.update_xml(f)

        self.assertTrue(self.overlay.file, 'Overlay should contain an XML.')

        self.assertTrue(self.overlay.file.size, 'Should be non-empty')

    def test_create_with_xml(self):
        overlay = Overlay.objects.create(page=self.page)
        with open(FILENAME_XML, 'rb') as f:
            overlay.update_xml(f)

        s_overlay = overlay.file.file.read()
        with open(FILENAME_XML, 'rb') as f:
            s_xml = f.read()
        self.assertEqual(s_xml, s_overlay, 'Should have identical content.')


class GeojsonTest(TransactionTestCase):
    """
    Test module for Geojson model
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
            width=10,
            height=20,
            document=self.doc
        )
        with open(FILENAME_IMAGE, 'rb') as f:
            self.page.update_image(f)

        self.overlay = Overlay.objects.create(
            page=self.page
        )

    def test_create(self):
        geojson = Geojson.objects.create(overlay=self.overlay,
                                         original=True,
                                         lang='en'
                                         )
        self.assertTrue(geojson)

    def test_create_obligatory(self):
        """
        There are some necessary parameters
        """

        overlay = self.overlay
        original = True
        lang = 'en'

        with self.subTest('SANITY CHECK. SHOULD PASS'):
            # Sanity check: The necessary parameters
            geojson = Geojson.objects.create(overlay=overlay,
                                             original=original,
                                             lang=lang
                                             )
            self.assertTrue(geojson)

        with self.subTest('No parameters'):
            try:
                geojson = Geojson.objects.create()
            except IntegrityError as e:
                # Expected behaviour
                pass
            else:
                self.fail('Should have failed.')

        with self.subTest('No overlay'):
            try:
                geojson = Geojson.objects.create(
                    original=original,
                    lang=lang
                )
            except IntegrityError as e:
                # Expected behaviour
                pass
            else:
                self.fail('Should have failed.')

        with self.subTest('No original'):
            try:
                geojson = Geojson.objects.create(
                    overlay=overlay,
                    lang=lang
                )
            except IntegrityError as e:
                # Expected behaviour
                pass
            else:
                self.fail('Should have failed.')

        with self.subTest('No lang'):
            try:
                geojson = Geojson.objects.create(
                    overlay=overlay,
                    original=original,
                )
            except IntegrityError as e:
                # Expected behaviour
                pass
            else:
                self.fail('Should have failed.')

    def test_load_file(self):
        geojson = Geojson.objects.create(overlay=self.overlay,
                                         original=True,
                                         lang='en'
                                         )

        self.assertFalse(geojson.file, 'Sanity check, start with no file.')

        # TODO change to geojson filename!
        with open(FILENAME_XML, 'rb') as f:
            geojson.update_file(f)

        self.assertTrue(geojson.file, 'geojson should contain a file.')

        self.assertTrue(geojson.file.size, 'Should be non-empty')

