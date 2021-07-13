import os
import warnings
from unittest import TestCase

import numpy as np
from PIL import Image

from documents.processing.file_upload import pdf_image_generator

ROOT_BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
DIR_FILETYPES = os.path.join(ROOT_BACKEND, 'tests/examples_data/filetypes')

FILENAME_PDF = os.path.join(DIR_FILETYPES, 'OCCAM Roadmap.pdf')
FILENAME_JPG = os.path.join(DIR_FILETYPES, 'OCCAM Roadmap.jpg')

if not os.path.exists(DIR_FILETYPES):
    warnings.warn(f"Couldn't find dir, {DIR_FILETYPES}", UserWarning)


class TestFoo(TestCase):

    def setUp(self) -> None:
        self.im_jpg = Image.open(FILENAME_JPG)

    def test_foo(self):
        """
        Input a pdf, output list of images
        Input:
            Path to PDF or the file? What is the most useful?
            Perhaps see what works for both
        Output:
            Again, save it somewhere or export as iterator that contains PIL.Images?
            PIL Images sounds more reasonable, just have to make sure it's convenient to save
            (to both file and django object)

        Returns:

        """
        pdf_image_generator(None)
        self.assertEqual(0, 1)

    def test_path(self):
        g = pdf_image_generator(FILENAME_PDF)

        im = next(g)

        self.assertTrue(im)

        a = np.asarray(im)
        a_jpg = np.asarray(self.im_jpg)

        np.mean(np.abs(a - a_jpg))

        self.assertEqual(a,
                         a_jpg,
                         'Not identical')

    def test_file(self):
        with open(FILENAME_PDF, 'rb') as f:
            g = pdf_image_generator(f.read())

        im = next(g)

        self.assertTrue(im)

        a = np.asarray(im)
        a_jpg = np.asarray(self.im_jpg)

        self.assertEqual(a,
                         a_jpg,
                         'Not identical')
