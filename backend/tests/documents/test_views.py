import os

from django.test import TestCase
from rest_framework import status

from backend.tests.documents.create_database_mock import create, login
from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from documents.views import OverlayTranslationView, PageTranscriptionView

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

B_DEBUG = True  # TODO Change to False in production


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
        url = '/documents/api/documents/'
        response = self.client_object.get(url)

        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllPagesTest(TestCase):
    """ Test module for GET all pages API """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_get_all_images(self):
        # get API response
        url = '/documents/api/pages'  # Without the '/'!
        response = self.client_object.get(url)

        images = Page.objects.all()
        serializer = PageSerializer(images, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllOverlaysTest(TestCase):
    """ Test module for GET all overlays API """

    url = '/documents/api/overlays/'

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_get_all_overlays(self):
        # get API response

        response = self.client_object.get(self.url)

        overlays = Overlay.objects.all()
        serializer = OverlaySerializer(overlays, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_overlay(self, b_debug=B_DEBUG):
        page = Page.objects.all()[0]

        filename_xml = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')

        with open(filename_xml, 'r') as f:
            # files= {'xml': f}
            response = self.client_object.post(self.url,
                                               data={'page': page.id,
                                                     'xml': f
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

    url = '/documents/api/overlay/translation'

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_post(self):
        # get API response

        overlay = Overlay.objects.exclude(file='')[0]

        if 1:
            response = self.client_object.post(self.url,
                                               data={'id': overlay.id,
                                                     'source': 'nl',
                                                     'target': 'en'
                                                     })
        else:
            v = OverlayTranslationView()
            response = v.post(None)

        # Get it again, to make sure it's updated.
        overlay_after = Overlay.objects.get(id=overlay.id)
        with overlay_after.file.open() as f:
            b_xml = f.read()

        self.assertLess(response.status_code, 300)
        self.assertEqual(response.data, b_xml)


class PageTranscriptionViewTest(TestCase):
    url = '/documents/api/page/transcription/'

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_post(self):
        # get API response

        page = next(filter(lambda x: 'jpg' in x.file.name, Page.objects.all())
                    )

        data = {'id': page.id,
                }

        if 1:
            response = self.client_object.post(self.url,
                                               data=data)
        else:
            v = PageTranscriptionView()

            class RequestMock:
                def __init__(self):
                    self.data = data

            response = v.post(RequestMock())

        self.assertLess(response.status_code, 300)
