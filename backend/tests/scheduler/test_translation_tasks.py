import os

from django.test import TestCase

from backend.tests.documents.create_database_mock import create, login
from documents.models import Overlay, Geojson
from scheduler.translation_tasks import translate_overlay

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
FILENAME_XML = os.path.join(ROOT, 'backend/tests/examples_data/page_minimal_working_example.xml')


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

        translate_overlay(overlay.id,
                          'nl',
                          'en')

    def test_create_geojson(self):
        source = 'NL'
        target = 'EN'

        overlay = next(filter(lambda x: 'xml' in x.file.name.lower(), Overlay.objects.all()))

        geojson_0 = list(Geojson.objects.all())
        n_geojson_0 = len(geojson_0)

        translate_overlay(overlay.id,
                          source,
                          target)

        n_geojson_1 = len(Geojson.objects.all())
        # Get the newest Geojson object.
        s_geojson_new = set(Geojson.objects.all()) - set(geojson_0)

        with self.subTest('Number of new geojsons'):
            self.assertEqual(n_geojson_0 + 1, n_geojson_1, 'Should be increased by one.')
            self.assertGreaterEqual(len(s_geojson_new), 1, 'Sanity check')

        geojson = list(s_geojson_new)[0]

        with self.subTest('source lang'):
            self.assertEqual(geojson.overlay.source_lang, source)

        with self.subTest('target lang'):
            self.assertEqual(geojson.lang, target)
