import os

from django.test import TestCase

from backend.tests.documents.create_database_mock import create, login
from documents.translation_connector import CEFeTranslationConnector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/page_minimal_working_example.xml')


class CEFeTranslationConnectorTest(TestCase):
    """
    """

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

        self.conn = CEFeTranslationConnector()

    def test_translate_file(self):
        source = 'fr'
        target = 'en'

        with open(FILENAME_XML, 'rb') as f:
            xml_trans = self.conn.translate_xml(f,
                                                source,
                                                target)

        self.assertTrue(xml_trans)

    def test_translate_file_non_blocking(self):
        source = 'fr'
        target = 'en'

        with open(FILENAME_XML, 'rb') as f:
            xml_id = self.conn.translate_xml_post(f,
                                                  source,
                                                  target)

        with self.subTest('POST response'):
            self.assertTrue(xml_id)

        xml_trans = self.conn.translate_xml_get(xml_id)

        with self.subTest('get response'):
            self.assertTrue(xml_trans)
