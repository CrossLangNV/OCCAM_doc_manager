from django.test import TransactionTestCase

from documents.models import LayoutAnalysisModel
from documents.ocr_connector import get_engines
from documents.ocr_engines import init_engines, _nice_string


class NiceStringTest(TransactionTestCase):  # Does not have to be a Django test, but will give import errors otherwise.
    def test_same(self):
        s = "This should stay the same"

        self.assertEqual(_nice_string(s), s)

    def test_remove_underscore(self):
        s = "Hello_world"
        s_expected = "Hello world"

        self.assertEqual(_nice_string(s), s_expected)

    def test_capitalise(self):
        s = "the world is round."
        s_expected = "The world is round."

        self.assertEqual(_nice_string(s), s_expected)

    def test_capitalise_abbreviation(self):
        s = "OCR"
        s_expected = "OCR"

        self.assertEqual(_nice_string(s), s_expected)

    def test_capitalize_and_remove_underscore(self):
        s = "a_very_boring_sentence"
        s_expected = "A very boring sentence"

        self.assertEqual(_nice_string(s), s_expected)


class LayoutAnalysisModelTest(TransactionTestCase):
    def test_init(self):
        name = "OCR model 0"
        value = "This extracts the text out of an image."

        config = [{'a': 1}, {}]

        layout_anlysis_model_i = LayoutAnalysisModel.objects.create(name=name,
                                                                    description=value,
                                                                    config=config)

        layout_anlysis_models = LayoutAnalysisModel.objects.all()

        self.assertIn(
            layout_anlysis_model_i, layout_anlysis_models, "Should have been constructed and saved in Django."
        )

        with self.subTest('name'):
            self.assertEqual(layout_anlysis_model_i.name, name)

        with self.subTest('description'):
            self.assertEqual(layout_anlysis_model_i.description, value)

        with self.subTest('config'):
            self.assertEqual(layout_anlysis_model_i.config, config)

    def test_init_when_emtpy(self):
        """
        When there are no models, they should be initialised with the ones from the config.

        Returns:

        """

        # Make sure it's empty
        LayoutAnalysisModel.objects.all().delete()

        items = LayoutAnalysisModel.objects.all()
        self.assertFalse(items, "Sanity check. Should be empty.")

        init_engines()

        self._engines_available()

    def test_init_when_full(self):
        """
        When all desired engines are already there, nothing should change.
        Returns:

        """

        # Start from all engines available
        init_engines()
        items0 = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Sanity check"):
            self.assertTrue(items0, "Should be non-empty.")

        init_engines()
        items1 = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Same items"):
            self.assertListEqual(items0, items1, "Should contain the exact same items.")

        with self.subTest("All engines available"):
            self._engines_available()

    def test_init_when_full_updating(self):
        """
        When all desired engines are already there, nothing should change.
        Returns:

        """

        # Start from all engines available
        init_engines()

        description_backup = {}
        for item in LayoutAnalysisModel.objects.all():
            description = item.description

            description_backup[item.name] = description
            # Reverse it or make non-empty
            item.description = description[::-1] if description else 'Empty description'

            item.save()

        items_before = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Sanity check: scrambled description"):
            for item in items_before:
                self.assertNotEqual(item.description, description_backup.get(item.name))

        # Actual start of the test.
        init_engines()
        items_after = list(LayoutAnalysisModel.objects.all())

        self.assertListEqual(items_before, items_after, "Should contain the exact same items.")

        with self.subTest("Restored description"):
            for item in items_after:
                self.assertEqual(item.description, description_backup.get(item.name))

        with self.subTest("All engines available"):
            self._engines_available()

    def test_init_partially(self):
        """
        If part of the engines are already there, only those missing should be added/updated.

        Returns:

        """

        # Start from all engines available and we remove one
        init_engines()
        items_before = list(LayoutAnalysisModel.objects.all())

        items_before[0].delete()
        items_min_one = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Sanity check"):
            self.assertEqual(len(items_min_one) + 1, len(items_before), "Should have removed one.")

        # Actual start of the test
        init_engines()
        items_after = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Restored to before"):
            f = lambda item: item.name
            self.assertListEqual(
                list(map(f, items_before)), list(map(f, items_after)), "Should contain the exact same items."
            )

        with self.subTest("All engines available"):
            self._engines_available()

    def test_init_with_others(self):
        """
        When other engines are added, they should be kept, and only those missing from the default are added.

        """

        # Start from all engines available and we remove one and we'll add 2.
        init_engines()
        items_before = list(LayoutAnalysisModel.objects.all())

        items_before[0].delete()
        items_min_one = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Sanity check, 1 gone"):
            self.assertEqual(len(items_min_one) + 1, len(items_before), "Should have removed one.")

        l_items_expected = []
        l_items_expected.extend(items_before)

        def add_tmp(name):
            tmp_engine_i = LayoutAnalysisModel.objects.create(name=name)
            tmp_engine_i.save()
            l_items_expected.append(tmp_engine_i)

        add_tmp("tmp engine 1")
        add_tmp("tmp engine 2")

        with self.subTest("Sanity check, 2 added"):
            self.assertEqual(len(LayoutAnalysisModel.objects.all()) - 2, len(items_min_one), "Should have added two.")

        # Actual start of the test
        init_engines()

        items_after = list(LayoutAnalysisModel.objects.all())

        with self.subTest("Restored to before"):
            f = lambda item: item.name
            self.assertListEqual(
                list(map(f, l_items_expected)), list(map(f, items_after)), "Should contain the exact same items."
            )

        with self.subTest("All engines available"):
            self._engines_available()

    def test_object_info_for_each_engine(self):
        """

        Returns:

        """
        # Actual start of the test
        init_engines()

        layout_anlysis_models = LayoutAnalysisModel.objects.all()
        layout_anlysis_models_names = [e.name for e in layout_anlysis_models]

        engines = get_engines()
        for engine_name, engine_info in engines.items():
            engine_name = _nice_string(engine_name)
            with self.subTest(f"Engine available in Django: {engine_name}"):
                self.assertIn(engine_name, layout_anlysis_models_names)

            with self.subTest("Config"):
                item = LayoutAnalysisModel.objects.get(name=engine_name)

                self.assertLessEqual(engine_info.items(), item.config.items())

    def _engines_available(self) -> None:
        layout_anlysis_models = LayoutAnalysisModel.objects.all()
        layout_anlysis_models_names = [e.name for e in layout_anlysis_models]

        engines = get_engines()
        for engine_name, engine_info in engines.items():
            with self.subTest(f"Engine available in Django: {engine_name}"):
                self.assertIn(_nice_string(engine_name), layout_anlysis_models_names)
