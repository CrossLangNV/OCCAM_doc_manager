"""
Test if create_database_mock.py behaves as expected
"""
import os

from django.http.response import HttpResponseRedirectBase, HttpResponseBase
from django.test import TestCase, Client

from documents.models import Page, Overlay
from tests.documents.create_database_mock import create, login, FILENAME_IMAGE, FILENAME_XML


class TestLogin(TestCase):
    def test_login(self):
        client, user = login()

        response = _client_get_with_redirect(client, "")
        self.assertLess(response.status_code, 300, "Failed attempt to get to homepage")

    def test_login_self(self):
        client, user = login(self)

        response = _client_get_with_redirect(client, "")
        self.assertLess(response.status_code, 300, "Failed attempt to get to homepage")


class TestCreate(TestCase):

    def tearDown(self) -> None:
        """
        Shared tests post creation

        Returns:
        """
        l_page_filenames = [page.file.name for page in Page.objects.all()]
        l_overlay_filenames = [overlay.file.name for overlay in Overlay.objects.all()]

        _, FILEBASE_IMAGE = os.path.split(FILENAME_IMAGE)
        _, FILEBASE_XML = os.path.split(FILENAME_XML)

        from unittest.util import safe_repr

        def assert_in_substring(filename_member, filenames, msg=None):
            """
            '19154766-page0.jpg' is defined as IN ['pages/19154766-page0_DANgHI5.jpg']
            this because we can ignore the random string at the end.

            """

            basename_member, ext_member = _get_base_ext(filename_member)

            for filename_with_index in filenames:
                basename_with_index, ext_with_index = _get_base_ext(filename_with_index)

                if basename_member in basename_with_index and ext_member == ext_with_index:
                    # Found a match
                    return

            standardMsg = '%s not found in %s' % (safe_repr(filename_member),
                                                  safe_repr(filenames))
            self.fail(self._formatMessage(msg, standardMsg))

        def assert_not_in_substring(filename_member, filenames, msg=None):
            """
            '19154766-page0.jpg' is defined as IN ['pages/19154766-page0_DANgHI5.jpg']
            this because we can ignore the random string at the end.

            """

            def _get_base_ext(filename):
                _, filebase = os.path.split(filename)
                basename, ext = os.path.splitext(filebase)

                return basename, ext

            basename_member, ext_member = _get_base_ext(filename_member)

            for filename_with_index in filenames:
                basename_with_index, ext_with_index = _get_base_ext(filename_with_index)

                if basename_member in basename_with_index and ext_member == ext_with_index:
                    # Found a match, thus fail

                    standardMsg = '%s not found in %s' % (safe_repr(filename_member),
                                                          safe_repr(filenames))
                    self.fail(self._formatMessage(msg, standardMsg))

            # No match found
            return

        with self.subTest('Image in page'):
            assert_in_substring(FILENAME_IMAGE, l_page_filenames, 'Expected this image in the pages')

        with self.subTest('XML in page'):
            assert_not_in_substring(FILENAME_XML, l_page_filenames, 'Should not be possible to upload XML to the pages')

        with self.subTest('XML in overlay'):
            assert_in_substring(FILENAME_XML, l_overlay_filenames, 'Expected this XML in the overlays')

    def test_create(self):
        create()

    def test_create_with_login(self):
        client, user = login()
        create(client)

    def test_create_with_login_self(self):
        client, user = login(self)
        create(client)


def _client_get_with_redirect(client: Client, path, *args, **kwargs) -> HttpResponseBase:
    """
    E.g. for the login, it gets redirected.

    Args:
        client:
        path:
        *args:
        **kwargs:

    Returns:
        Response after going through all redirecting.
    """

    response = client.get(path, *args, **kwargs)

    if isinstance(response, HttpResponseRedirectBase):
        path_redirect = response.url

        return _client_get_with_redirect(client, path_redirect, *args, **kwargs)

    return response


def _get_base_ext(filename):
    _, filebase = os.path.split(filename)
    basename, ext = os.path.splitext(filebase)

    return basename, ext
