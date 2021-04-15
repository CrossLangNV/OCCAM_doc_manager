from django.contrib.auth.models import User
from django.test import TestCase, Client
from rest_framework import status

from documents.models import Document, Image
from documents.serializers import DocumentSerializer, ImageSerializer
from tests.backend.documents.create_database_mock import create


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

        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
