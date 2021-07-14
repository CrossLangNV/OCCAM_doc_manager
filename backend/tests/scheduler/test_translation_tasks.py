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
        self.client, self.user = login(self)
        self.content_type = 'application/json'

        create(client=self.client)

    def test_call(self):
        overlay = Overlay.objects.all()[0]
        with open(FILENAME_XML, 'rb') as f:
            overlay.update_xml(f)

        source = overlay.source_lang
        target = 'EN'
        self.assertNotEqual(source, target, 'Sanity check. Should be translated to a different language.')

        translate_overlay(overlay.pk,
                          target
                          )

        with self.subTest('Translation file'):
            self.assertTrue(overlay.translation_file, 'should add a translation.')

        with self.subTest('Geojson'):
            self.assertTrue(overlay.overlay_geojson.filter(original=False),
                            'should add a translated geojson.')

    def test_call_with_user(self):

        overlay = Overlay.objects.all()[0]
        with open(FILENAME_XML, 'rb') as f:
            overlay.update_xml(f)

        source = overlay.source_lang
        target = 'EN'
        self.assertNotEqual(source, target, 'Sanity check. Should be translated to a different language.')

        translate_overlay(overlay.pk,
                          target,
                          user_pk=self.user.pk
                          )

        with self.subTest('Translation file'):
            self.assertTrue(overlay.translation_file, 'should add a translation.')

        with self.subTest('Geojson'):
            self.assertTrue(overlay.overlay_geojson.filter(original=False),
                            'should add a translated geojson.')

    def test_create_geojson(self):
        overlay = next(filter(lambda x: 'xml' in x.file.name.lower(), Overlay.objects.all()))

        source = overlay.source_lang
        target = 'EN'
        self.assertNotEqual(source, target, 'Sanity check')

        geojson_0 = list(Geojson.objects.all())
        n_geojson_0 = len(geojson_0)

        translate_overlay(overlay.pk,
                          target
                          )

        with self.subTest('Geojson'):
            self.assertTrue(overlay.overlay_geojson.filter(original=False),
                            'should add a translated geojson.')

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

    def test_same_source_target_language(self):
        overlay = Overlay.objects.all()[0]
        with open(FILENAME_XML, 'rb') as f:
            overlay.update_xml(f)

        source = overlay.source_lang

        try:
            translate_overlay(overlay.pk,
                              source
                              )
        except Exception as e:
            self.assertTrue(e, 'Should fail on source to source translation')

        else:
            self.fail('Should fail on source to source translation')
