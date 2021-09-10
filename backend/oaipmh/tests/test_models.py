import unittest

from oaipmh.models import Community


class TestConnectorDSpaceRESTInit(unittest.TestCase):
    def test_from_dict(self):
        d = {"id": 123, "name": "Reports Community"}

        community = Community(**d)

        self.assertTrue(community)
