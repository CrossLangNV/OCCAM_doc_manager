"""
Test if create_database_mock.py behaves as expected
"""

from django.test import TestCase

from documents.models import Page, Overlay
from tests.documents.create_database_mock import create, login, FILENAME_IMAGE, FILENAME_XML


class TestLogin(TestCase):
    def test_login(self):
        client, user = login()

        response = client.get("")
        self.assertLess(response.status_code, 300, "Failed attempt to get to homepage")

    def test_login_self(self):
        client, user = login(self)

        response = client.get("")
        self.assertLess(response.status_code, 300, "Failed attempt to get to homepage")


class TestCreate(TestCase):

    def tearDown(self) -> None:
        """
        Shared tests post creation

        Returns:
        """
        l_page_filenames = [page.file.name for page in Page.objects.all()]
        l_overlay_filenames = [overlay.file.name for overlay in Overlay.objects.all()]

        with self.subTest('Image in page'):
            self.assertIn(FILENAME_IMAGE, l_page_filenames, 'Expected this image in the pages')

        with self.subTest('XML in page'):
            self.assertIn(FILENAME_XML, l_page_filenames, 'Expected this XML in the pages')

        with self.subTest('XML in overlay'):
            self.assertIn(FILENAME_XML, l_overlay_filenames, 'Expected this XML in the overlays')

    def test_create(self):
        create()

    def test_create_with_login(self):
        client, user = login()
        create(client)

    def test_create_with_login_self(self):
        client, user = login(self)
        create(client)
