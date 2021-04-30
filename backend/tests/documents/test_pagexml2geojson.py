import os
import unittest

from documents.pagexml2geojson import main, lxml_text_region_iterator, lxml_text_region_iterator_trans

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FILENAME = os.path.join(ROOT, 'examples_data/KB_JB840_1919-04-01_01_0.xml')
FILENAME_MULTI = os.path.join(ROOT, 'examples_data/KB_JB840_1919-04-01_01_0_trans_multi.xml')


class TestFoo(unittest.TestCase):
    def test_bar(self):
        d = main(FILENAME)

        self.assertTrue(d)

    def test_multilingual(self):
        d_baseline = main(FILENAME)

        d_multi = main(FILENAME_MULTI)

        self.assertTrue(d_multi, 'Sanity check. Should return something')
        self.assertGreaterEqual(len(d_multi['features']), 1, 'Sanity check. Should return multiple elements')

        self.assertEqual(len(d_baseline['features']), len(d_multi['features']))

        with self.subTest('Equal string values'):
            for i, (f, f_multi) in enumerate(zip(d_baseline['features'], d_multi['features'])):
                self.assertEqual(f, f_multi, f'Line {i}. Should be equal.')

    def test_get_trans(self):
        l_baseline = list(lxml_text_region_iterator(FILENAME_MULTI))

        l_trans = list(lxml_text_region_iterator_trans(FILENAME_MULTI, 'fr'))

        self.assertTrue(l_trans, 'Sanity check. Should return something')
        self.assertGreaterEqual(len(l_trans), 1, 'Sanity check. Should return multiple elements')

        self.assertEqual(len(l_baseline), len(l_trans))
