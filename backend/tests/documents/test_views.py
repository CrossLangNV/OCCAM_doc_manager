import os

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from backend.tests.documents.create_database_mock import create, login, FILENAME_IMAGE
from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from tests.documents.test_create_database_mock import _get_base_ext

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))

B_DEBUG = False

URL_DOCUMENTS = '/documents/api/documents'
URL_PAGES = '/documents/api/pages'
URL_OVERLAYS = '/documents/api/overlays'
URL_TRANSLATION = '/documents/api/pages/translate'
URL_TRANSCRIPTION = '/documents/api/pages/launch_ocr'

FILENAME_PAGE_PDF = os.path.join(ROOT, 'backend/tests/examples_data/filetypes/OCCAM Roadmap.pdf')
FILENAME_PAGE_PNG = os.path.join(ROOT, 'backend/tests/examples_data/filetypes/OCCAM Roadmap.png')
FILENAME_PAGE_JPG = os.path.join(ROOT, 'backend/tests/examples_data/filetypes/OCCAM Roadmap.jpg')


class GetAllDocumentsTest(APITestCase):
    """ Test module for GET all documents API """

    def setUp(self):
        self.client, self.user = login()
        create(client=self.client,
               user=self.user)

    def test_get_all_documents(self):
        # get API response

        response = self.client.get(URL_DOCUMENTS)

        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_post_document(self):
        documents_before = list(Document.objects.all())

        response = self.client.post(URL_DOCUMENTS,
                                    data={'name': 'post document'
                                          }
                                    )

        with self.subTest('Status code'):
            self.assertIn(response.status_code, (status.HTTP_200_OK,
                                                 status.HTTP_201_CREATED))

        documents = Document.objects.all()

        with self.subTest('New document'):
            self.assertEqual(len(documents), len(documents_before) + 1,
                             'Number of documents should have increased by one.')


class GetAllPagesTest(TestCase):
    """ Test module for GET all pages API """

    def setUp(self):
        self.client, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client)

    def test_get_all_images(self):
        # get API response

        response = self.client.get(URL_PAGES)

        images = Page.objects.all()
        serializer = PageSerializer(images, many=True)

        self.assertEqual(response.data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_image(self):
        doc_0 = Document.objects.all()[0]

        pages_before = list(Page.objects.all())

        with open(FILENAME_IMAGE, "rb") as f:
            response = self.client.post(URL_PAGES,
                                        data={"document": doc_0.id,
                                              "file": f,
                                              },
                                        format="multipart",
                                        )

        with self.subTest('Status code'):
            self.assertIn(response.status_code, (status.HTTP_200_OK,
                                                 status.HTTP_201_CREATED))

        pages = Page.objects.all()

        with self.subTest('New page'):
            self.assertEqual(len(pages), len(pages_before) + 1, 'Number of pages should have increased by one.')

    def test_upload_pdf(self) -> None:
        """
        When uploading a PDF, it should be converted to a set of images and save as multiple pages.

        Returns:
            None
        """

        doc_0 = Document.objects.all()[0]

        pages_before = list(Page.objects.all())

        with open(FILENAME_PAGE_PDF, "rb") as f:
            response = self.client.post(URL_PAGES,
                                        data={"document": doc_0.id,
                                              "file": f,
                                              },
                                        format="multipart",
                                        )

        with self.subTest('Status code'):
            self.assertIn(response.status_code, (status.HTTP_200_OK,
                                                 status.HTTP_201_CREATED))

        pages = Page.objects.all()
        pages_new = list(filter(lambda page: page not in pages_before, pages))

        with self.subTest('New page'):
            self.assertEqual(len(pages), len(pages_before) + 1, 'Number of pages should have increased by one.')
            self.assertEqual(len(pages_new), 1, 'Number of pages should have increased by one.')

        with self.subTest('PDF converted to JPG'):
            page_new = pages_new[0]

            page_new_base, page_new_ext = _get_base_ext(page_new.file.name)
            jpg_base, jpg_ext = _get_base_ext(FILENAME_PAGE_JPG)

            self.assertEqual(page_new_ext, jpg_ext)
            self.assertIn(jpg_base.replace(' ', '_'),
                          page_new_base.replace(' ', '_'))

        return


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
                                                     'file': f,
                                                     },
                                               format="multipart",
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
        self.client, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client)

    def test_post(self):
        # get API response

        overlay = Overlay.objects.exclude(file='')[0]

        response = self.client.post(URL_TRANSLATION,
                                    data={'overlay': overlay.id,
                                          'target': 'en'
                                          })

        # Get it again, to make sure it's updated.
        overlay_after = Overlay.objects.get(pk=overlay.pk)
        with overlay_after.translation_file.open() as f:
            b_xml = f.read()

        self.assertLess(response.status_code, 300)

        with self.subTest('Translated overlay available'):
            self.assertTrue(b_xml, 'Should be non-empty')


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
