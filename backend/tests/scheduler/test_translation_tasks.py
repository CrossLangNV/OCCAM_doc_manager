import os

from django.test import TestCase

from backend.tests.documents.create_database_mock import create, login
from documents.models import Overlay
from scheduler.translation_tasks import translate_overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/KB_JB840_1919-04-01_01_0.xml')


class TranslateOverlayTest(TestCase):
    """
    """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

    def test_call(self):
        overlay = Overlay.objects.all()[0]
        with open(FILENAME_XML, 'rb') as f:
            overlay.update_xml(f)

        r = translate_overlay(overlay.id,
                              'nl',
                              'en')

        self.assertTrue(r)
