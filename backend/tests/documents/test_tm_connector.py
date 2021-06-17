import os

from django.test import TestCase

from backend.tests.documents.create_database_mock import create, login
from documents.tm_connector import MouseTmConnector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FILENAME_TMX = os.path.join(ROOT, 'backend/tests/examples_data/en-nl_min.tmx')


class MouseTmConnectorTest(TestCase):

    def setUp(self):
        self.client_object, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client_object)

        self.conn = MouseTmConnector()

    def test_health(self):
        response = self.conn.health_check()
        print(response)

    def test_lookup_tu(self):
        response = self.conn.lookup_tu(False, '', 'en-nl', 'this is a test')
        print(response)

    def test_add_tu(self):
        response = self.conn.add_tu('', 'en-nl', 'this is a test', 'dit is een test')
        print(response)

    def test_import_tmx(self):
        response = self.conn.import_tmx('', 'en-nl', open(FILENAME_TMX, 'rb'))
        print(response)
