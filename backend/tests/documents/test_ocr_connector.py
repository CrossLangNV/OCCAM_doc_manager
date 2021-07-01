from django.test import TransactionTestCase

from documents.ocr_connector import get_engines, get_request_id, KEY_ENGINE_ID, KEY_MODELS, KEY_MODEL_ID, KEY_MODEL_NAME


class TestGetEngines(TransactionTestCase):

    def test_response_content(self):
        """
        Research about the different engines that are available through the PERO-OCR API.
        28/06/2021: Only 3 of the engines are available.

        """

        engines = get_engines()  # response_engines.get(key_engines)

        with self.subTest('Layout engines'):
            for engine_name, abc in engines.items():
                print(abc)

        for key_description in ['description',
                                'engine_version',
                                KEY_ENGINE_ID,
                                ]:

            with self.subTest(f'Engine {key_description}'):
                for engine_value in engines.values():
                    self.assertIn(key_description, engine_value, f'Should have a child with key: {key_description}')

        with self.subTest('Engine models'):
            for engine_value in engines.values():
                engine_models = engine_value.get(KEY_MODELS)

                for engine_model in engine_models:
                    self.assertIn(KEY_MODEL_ID, engine_model)
                    self.assertIn(KEY_MODEL_NAME, engine_model)

        with self.subTest('Engine model names'):
            # This seems to include:
            # * layout_models (first step)
            # * OCR engine
            # * Language model (Optional)
            for engine_name, engine in engines.items():
                print('Engine:', engine_name)
                print('\tmodels:')
                for model_name in map(lambda model: model.get(KEY_MODEL_NAME), engine.get(KEY_MODELS)):
                    print(f'\t * {model_name}')


class TestDifferentEngines(TransactionTestCase):

    def test_get_request_id_for_different_engines(self, b_debug=False) -> None:
        """
        Conclusion: Only the engine id's work that do the whole pipeline (Layout analysis + OCR)

        Args:
            b_debug:
                Also tests
                * the separate layout analysis and OCR model's indices.
                * Other id's

        Returns:
            None
        """

        page_id = 'page_id_tmp'

        with self.subTest("with engine id's"):

            for id in _engine_id_generator():
                with self.subTest(f" * engine {id}"):
                    r_id = get_request_id(page_id,
                                          pero_engine_id=id)

                    self.assertTrue(r_id)

        if b_debug:

            with self.subTest("with model id's"):
                for id in _model_id_generator():
                    with self.subTest(f" * model {id}"):
                        r_id = get_request_id(page_id,
                                              pero_engine_id=id)

                        self.assertTrue(r_id)

            with self.subTest("Try other id's"):

                l_id_engine = list(_engine_id_generator())
                l_id_model = list(_model_id_generator())

                for id in filter(
                        lambda id: (id not in l_id_engine) and (id not in l_id_model),
                        range(
                            max(
                                max(l_id_engine),
                                max(l_id_model)
                            )
                        )
                ):
                    with self.subTest(f" * id: {id}"):
                        r_id = get_request_id(page_id,
                                              pero_engine_id=id)

                        self.assertTrue(r_id)


def _engine_id_generator():
    engines = get_engines()

    for engine_info in engines.values():
        yield engine_info.get(KEY_ENGINE_ID)


def _model_id_generator():
    engines = get_engines()

    for _, engine_info in engines.items():
        for model_info in engine_info[KEY_MODELS]:
            yield model_info[KEY_MODEL_ID]
