import os

from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status

from backend.tests.documents.create_database_mock import create
from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, ImageSerializer, OverlaySerializer
from documents.views import OverlayTranslationView

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


class GetAllImagesTest(TestCase):
    """ Test module for GET all images API """

    def setUp(self):
        create()

        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

    def test_get_all_images(self):
        # get API response
        url = '/documents/api/images/'
        response = self.client_object.get(url)

        images = Page.objects.all()
        serializer = ImageSerializer(images, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAllOverlaysTest(TestCase):
    """ Test module for GET all overlays API """

    url = '/documents/api/overlays/'

    def setUp(self):
        create()

        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

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
        create()

        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

    def test_post(self):
        # get API response

        if 1:
            response = self.client_object.post(self.url)
        else:
            v = OverlayTranslationView()
            response = v.post(None)

        overlay0 = next(filter(lambda x: x.xml, Overlay.objects.all()))

        with overlay0.xml.open() as f:
            b_xml = f.read()

        self.assertTrue(response.ok)
        self.assertEqual(response.data, b_xml)


def login(self):
    username = 'dummy@gmail.com'
    password = 'Dummy@123'
    self.username = username
    self.password = password

    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()

    # initialize the APIClient app
    client = Client()
    b = client.login(username=username, password=password)
    assert b
    return client, user
