from django.test import TransactionTestCase

from backend.tests.documents.create_database_mock import create
from documents.models import Page, Label
from documents.serializers import PageSerializer


class PageSerializerTest(TransactionTestCase):
    def setUp(self) -> None:

        self.page_serializer = PageSerializer()

        create()

        self.page0 = Page.objects.all()[0]
        # Add a label
        self.label = Label(name="classifier", value="Epic model", page=self.page0)
        self.label.save()

    def test_get_metadata(self):
        d_meta = self.page_serializer.get_metadata(self.page0)

        with self.subTest("non-empty"):
            self.assertTrue(d_meta)

        with self.subTest("Titles"):
            self.assertIn("titles", d_meta)

        with self.subTest("Languages"):
            self.assertIn("languages", d_meta)

        with self.subTest("values are lists"):
            for value in d_meta.values():
                self.assertIsInstance(value, list)

    def test_get_metadata_xml(self):
        d_meta = self.page_serializer.get_metadata(self.page0)

        xml_meta = self.page_serializer.get_metadata_xml(self.page0)

        self.assertTrue(xml_meta)

        for key, values in d_meta.items():

            # TODO what to do with labels. Do we also want that in the DC XML?
            # Currently the labels do not have to be added to the XML.
            if key == self.label.name:
                continue

            with self.subTest(f"Values {key}"):
                for value in values:
                    self.assertIn(value, xml_meta, "Couldn't find metadata value in the XML.")

    def test_same_key_labels(self):
        """
        When there are two labels with the same key value, both values should be returned in the metadata
        Returns:

        """
        name = self.label.name

        # Add a label
        label2 = Label(name=name, value="A mediocre classifier", page=self.page0)
        label2.save()

        d_meta = self.page_serializer.get_metadata(self.page0)

        with self.subTest("Key"):
            self.assertIn(name, d_meta, "The label's name should be saved in the metadata")

        label_values = d_meta.get(name)

        with self.subTest("Old label value"):
            self.assertIn(self.label.value, label_values, "Should contain old label value")

        with self.subTest("New label value"):
            self.assertIn(label2.value, label_values, "Should contain new label value")
