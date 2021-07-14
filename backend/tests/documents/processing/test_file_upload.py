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


class TestPdfImageGenerator(TestCase):

    def setUp(self) -> None:
        self.im_jpg = Image.open(FILENAME_JPG)

    def test_pdf_image_generator_path(self):
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
        g = pdf_image_generator(FILENAME_PDF)

        im = next(g)

        with self.subTest('Return an image'):
            self.assertIsInstance(im, Image.Image, 'Expected a PIL image.')

        a = np.asarray(im)
        a_jpg = np.asarray(self.im_jpg)

        if 0:
            # TODO work on expected resizing
            self.assertEqual(a,
                             a_jpg,
                             'Not identical')

        with self.subTest('Similar aspect ratio'):
            ratio_jpg = a_jpg.shape[0] / a_jpg.shape[1]
            ratio = a.shape[0] / a.shape[1]

            self.assertAlmostEqual(ratio, ratio_jpg, delta=0.01, msg='Aspect ratio should be similar')

    def test_pdf_image_generator_file(self):
        with open(FILENAME_PDF, 'rb') as f:
            g = pdf_image_generator(f.read())

        im = next(g)

        with self.subTest('Return an image'):
            self.assertIsInstance(im, Image.Image, 'Expected a PIL image.')

        a = np.asarray(im)
        a_jpg = np.asarray(self.im_jpg)

        if 0:
            # TODO work on expected resizing
            self.assertEqual(a,
                             a_jpg,
                             'Not identical')

        with self.subTest('Similar aspect ratio'):
            ratio_jpg = a_jpg.shape[0] / a_jpg.shape[1]
            ratio = a.shape[0] / a.shape[1]

            self.assertAlmostEqual(ratio, ratio_jpg, delta=0.01, msg='Aspect ratio should be similar')
