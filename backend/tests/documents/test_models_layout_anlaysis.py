from django.test import TransactionTestCase

from documents.models import LayoutAnalysisModel


class LayoutAnalysisModelTest(TransactionTestCase):
    def test_init(self):
        name = 'OCR model 0'
        value = 'This extracts the text out of an image.'

        LayoutAnalysisModel.objects.create(
            name=name,
            value=value
        )
