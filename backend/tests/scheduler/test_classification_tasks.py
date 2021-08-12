import os

from django.test import TransactionTestCase

from scheduler.classification_tasks import classify_scanned

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
# FILENAME_PDF = os.path.join(ROOT, "backend/tests/examples_data/KB_JB840_1919-04-01_01.pdf")
FILENAME_PDF = os.path.join(ROOT, "backend/tests/examples_data/annual_account_2007-04102846.pdf")

PREDICTION = "prediction"


class XMLLangDetectTest(TransactionTestCase):
    def test_(self):
        with open(FILENAME_PDF, 'rb') as f:
            r = classify_scanned(f)

        self.assertEqual(r[PREDICTION], False, 'The PDF was expected to not-scanned, and instead machine readable.')
