from django.test import TransactionTestCase

from documents.fixtures.engines_main import main, ENGINES_JSON


class FixturesGeneratorTest(TransactionTestCase):
    def test_foo(self):
        main()


class FixturesTest(TransactionTestCase):
    fixtures = [ENGINES_JSON]

    def test_bar(self):
        pass
