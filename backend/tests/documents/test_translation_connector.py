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
        self.source = 'fr'
        self.target = 'en'

        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

        self.conn = CEFeTranslationConnector()

    def test_translate_file(self):

        with open(FILENAME_XML, 'rb') as f:
            xml_trans = self.conn.translate_xml(f,
                                                self.source,
                                                self.target)

        self.assertTrue(xml_trans)

    def test_translate_file_non_blocking(self):

        with open(FILENAME_XML, 'rb') as f:
            xml_id = self.conn.translate_xml_post(f,
                                                  self.source,
                                                  self.target)

        with self.subTest('POST response'):
            self.assertTrue(xml_id)

        xml_trans = self.conn.translate_xml_get(xml_id)

        with self.subTest('get response'):
            self.assertTrue(xml_trans)

    def test_translate_source_to_source(self):

        with open(FILENAME_XML, 'rb') as f:
            try:
                xml_trans = self.conn.translate_xml(f,
                                                    self.source,
                                                    self.source)
            except Exception as e:
                self.assertTrue(e, 'Should raise an error about target being equal to source language.')

            else:
                self.fail(
                    'Should have raised an error immediately that target should be different than the source language.')
