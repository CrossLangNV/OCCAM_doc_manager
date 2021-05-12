import os

from django.test import TestCase
from rest_framework import status

from backend.tests.documents.create_database_mock import create, login
from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

B_DEBUG = True  # TODO Change to False in production

URL_DOCUMENTS = '/documents/api/documents/'
URL_PAGES = '/documents/api/pages/'
URL_OVERLAYS = '/documents/api/overlays/'
URL_TRANSLATION = '/documents/api/pages/translate'
URL_TRANSCRIPTION = '/documents/api/pages/launch_ocr'


class GetAllDocumentsTest(TestCase):
    """ Test module for GET all documents API """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        self.name = 'Declaration of Independence'
        self.content = 'Stolen by Nicolas Cage.'

        Document.objects.create(
            name=self.name,
            content=self.content
        )

        Document.objects.create(name='Document 2', content='Content 2.')

    def test_get_all_documents(self):
        # get API response
        response = self.client_object.get(URL_DOCUMENTS)

        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)


class GetAllPagesTest(TestCase):
    """ Test module for GET all pages API """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_get_all_images(self):
        # get API response

        response = self.client_object.get(URL_PAGES)

        images = Page.objects.all()
        serializer = PageSerializer(images, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllOverlaysTest(TestCase):
    """ Test module for GET all overlays API """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_get_all_overlays(self):
        # get API response
        response = self.client_object.get(URL_OVERLAYS)

        overlays = Overlay.objects.all()
        serializer = OverlaySerializer(overlays, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_overlay(self, b_debug=B_DEBUG):
        page = Page.objects.all()[0]

        filename_xml = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')

        with open(filename_xml, 'r') as f:
            # files= {'xml': f}
            response = self.client_object.post(URL_OVERLAYS,
                                               data={'page': page.id,
                                                     'xml': f,
                                                     'source_lang': 'NL'
                                                     },
                                               # files=files
                                               )
        if b_debug:
            print(response.data)

        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_201_CREATED))

        overlay_id = response.data.get('id')

        overlays = Overlay.objects.all()

        self.assertIn(overlay_id, list(map(lambda o: str(o.id), overlays)))


class OverlayTranslationViewTest(TestCase):
    """ Test module for GET all overlays API """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_post(self):
        # get API response

        overlay = Overlay.objects.exclude(file='')[0]

        response = self.client_object.post(URL_TRANSLATION,
                                           data={'overlay': overlay.id,
                                                 'source': 'nl',
                                                 'target': 'en'
                                                 })

        # Get it again, to make sure it's updated.
        overlay_after = Overlay.objects.get(id=overlay.id)
        with overlay_after.file.open() as f:
            b_xml = f.read()

        self.assertLess(response.status_code, 300)
        self.assertEqual(response.data, b_xml)


class PageTranscriptionViewTest(TestCase):
    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_post(self):
        # get API response

        page = next(filter(lambda x: 'jpg' in x.file.name, Page.objects.all())
                    )

        data = {'page': page.id,
                }

        response = self.client_object.post(URL_TRANSCRIPTION,
                                           data=data)

        self.assertLess(response.status_code, 300)
