import filecmp
import os
import tempfile
import unittest
import urllib

from oaipmh.connector import ConnectorDSpaceREST, XMLResponse
from oaipmh.models import ItemAdd, BitstreamAdd, CommunityAdd, CollectionAdd

"""7
Confluence documentation:
https://wiki.lyrasis.org/display/DSDOC6x/REST+API
"""

ROOT = os.path.join(os.path.dirname(__file__), '../..')

URL_DSPACE = os.environ['URL_DSPACE']
EMAIL = os.environ['EMAIL_DSPACE']
PASSWORD = os.environ['PASSWORD_DSPACE']


class TestConnectorDSpaceRESTInit(unittest.TestCase):
    def test_init(self):
        """
        Check if the connector can be called and doesn't crash

        :return:
        """
        with ConnectorDSpaceREST(URL_DSPACE) as connector:
            print(connector)


class TestConnectorDSpaceREST(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)

    def tearDown(self) -> None:
        self.connector.close()

    def test_login(self):
        JSESSIONID = self.connector.login(EMAIL, PASSWORD)

        self.assertTrue(JSESSIONID, "Should return something")
        self.assertIsInstance(JSESSIONID, str, "Should return the cookie session ID as a string")

    def test_get_communities(self):
        l = self.connector.get_communities()
        self.assertTrue(len(l), "Should return something")

    def test_get_collections(self):
        l = self.connector.get_collections()
        self.assertTrue(len(l), "Should return something")

    def test_get_items(self):
        l = self.connector.get_items()
        self.assertTrue(len(l), "Should return something")

    def test_get_bitstreams(self):
        l = self.connector.get_bitstreams()
        self.assertTrue(len(l), "Should return something")


class TestConnectorDSpaceRESTAddCommunity(unittest.TestCase):
    name = 'Demo model'

    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add_community(self):
        with self.subTest('Clear previous entries'):
            self._delete_community()

        community = CommunityAdd(name=self.name)
        self.connector.add_community(community)

        l = self.connector.get_communities()
        l_names = list(map(lambda community: community.name, l))

        self.assertIn(self.name, l_names)

    def _delete_community(self):
        l = self.connector.get_communities()

        for community in filter(lambda community: community.name == self.name, l):
            r = self.connector.delete_community(community.uuid)

            self.assertTrue(r)

        l = self.connector.get_communities()
        l_names = list(map(lambda community: community.name, l))

        self.assertFalse(self.name in l_names)


class TestConnectorDSpaceRESTAddCollection(unittest.TestCase):
    name = 'Demo document classifier'

    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

        self._add_collection()

    def tearDown(self) -> None:
        self._delete_collection()

        self.connector.close()

    def _add_collection(self):

        def get_community():
            l_community = self.connector.get_communities()

            for community in filter(lambda community: community.name == TestConnectorDSpaceRESTAddCommunity.name,
                                    l_community):
                return community

        community = get_community()

        collection = CollectionAdd(name=self.name)
        self.connector.add_collection(collection, community.uuid)

    def _delete_collection(self):

        l = self.connector.get_collections()

        for i, collection in enumerate(filter(lambda collection: collection.name == self.name, l)):
            if i == 0:
                # Keep 1 alive
                continue
            r = self.connector.delete_collection(collection.uuid)

            self.assertTrue(r)

    def test_add_collection(self):

        with self.subTest('Clear previous entries'):
            self._delete_collection()

        self._add_collection()
        l = self.connector.get_collections()

        l_names = list(map(lambda collection: collection.name, l))

        self.assertIn(self.name, l_names)

    def test_delete_collection(self):

        self._delete_collection()

        l = self.connector.get_collections()
        l_names = list(map(lambda collection: collection.name, l))

        l_names_filter = [name for name in l_names if self.name == name]
        self.assertLessEqual(len(l_names_filter), 1)


class TestConnectorDSpaceRESTAddItem(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)


    def tearDown(self) -> None:
        self.connector.close()

    def test_add_doc_classifier(self):
        collection0 = list(filter(lambda x: TestConnectorDSpaceRESTAddCollection.name in x.name, self.connector.get_collections()))[0]
        collection_id = collection0.uuid

        def get_item_create():
            d = {
                "name": "2015 Annual Report",
            }
            item = ItemAdd(**d)
            return item

        item = get_item_create()

        items_before = self.connector.get_items()

        xml = self.connector.add_item(item, collection_id)
        print(xml)

        items_after = self.connector.get_items()

        with self.subTest("One item is added"):
            self.assertEqual(len(items_before) + 1, len(items_after))

        get_uuid = lambda item: item.uuid
        l_uuid_before = list(map(get_uuid, items_before))
        l_uuid_after = list(map(get_uuid, items_after))
        l_diff = list(filter(lambda item: get_uuid(item) not in l_uuid_before, items_after))

        with self.subTest("One new item"):
            self.assertEqual(len(l_diff), 1)

        last_item = l_diff[0]

        with self.subTest("Equal text"):
            self.assertEqual(last_item.name, xml._get("name"))

        with self.subTest("Equal uuid"):
            self.assertEqual(last_item.uuid, xml.get_uuid())

        with self.subTest("Equal link"):
            self.assertEqual(last_item.link, xml.get_link())

        with self.subTest("Equal handle"):
            self.assertEqual(last_item.handle, xml.get_handle())

        for key in vars(item).keys():  # d.keys():
            with self.subTest(f"Equal item: {key}"):
                value_last_item = getattr(last_item, key)
                value_item = getattr(item, key)

                self.assertEqual(value_last_item, value_item)


class TestConnectorDSpaceRESTAddBitstream(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

    def tearDown(self) -> None:
        self.connector.close()

    def test_add(self):
        """
        Example code to delete the item:
        >> self.connector.delete_item(item0_uuid)
        """

        bitstream = BitstreamAdd(
            name="Document classification model for NBB vs Belgian Official Gazette. Tensorflow model."
        )

        bitstreams_before = self.connector.get_bitstreams()

        item0_uuid = _get_temp_item(self.connector)

        import os
        # filename = os.path.join(os.path.dirname(__file__), 'example_files/model_nbb_bris.h5')
        filename = os.path.join(os.path.dirname(__file__), 'example_files/kaligrafie.jpg')
        basename = os.path.split(filename)[-1]

        description = 'this a description'

        with open(filename, 'rb') as file:
            r = self.connector.add_bitstream(file,
                                             basename,
                                             item0_uuid,
                                             description=description)

        self.assertTrue(r)

        bitstreams_after = self.connector.get_bitstreams()

        f_uuid = lambda x: x.uuid
        bitstreams_uuid_before = list(map(f_uuid, bitstreams_before))
        bitstreams_delta = list(filter(lambda x: f_uuid(x) not in bitstreams_uuid_before, bitstreams_after))

        with self.subTest('number of new bitstreams'):
            self.assertEqual(len(bitstreams_delta), 1, 'Should only add one')

        new_bitstream = bitstreams_delta[0]

        with self.subTest('Equal name'):
            self.assertEqual(new_bitstream.name, basename)

        with self.subTest('Equal description'):
            self.assertEqual(new_bitstream.description, description)

        url_file = URL_DSPACE + new_bitstream.retrieveLink

        with tempfile.TemporaryDirectory() as tmp_dir:
            filename_tmp = os.path.join(tmp_dir, new_bitstream.name)
            urllib.request.urlretrieve(url_file, filename_tmp)

            with self.subTest('Same file content'):
                check = filecmp.cmp(filename, filename_tmp)  # r.content)

                self.assertTrue(check, 'Content should be the same')

        return


class TestConnectorDSpaceRESTdelete(unittest.TestCase):
    def setUp(self) -> None:
        # Instead of using a with statement, it is closed in the teardown.
        self.connector = ConnectorDSpaceREST(URL_DSPACE)
        self.connector.login(EMAIL, PASSWORD)

        self.connector_readonly = ConnectorDSpaceREST(URL_DSPACE)

    def tearDown(self) -> None:
        self.connector.close()
        self.connector_readonly.close()

    def test_delete_item(self):
        # Get all items that I want to delete

        items = self.connector.get_items()

        def f_filter(item):
            return (item.name is None) or ("2015 Annual Report" in item.name)

        for item in filter(f_filter, items):
            self.connector.delete_item(item.uuid)

        items_after = self.connector.get_items()
        items_after_filter = list(filter(f_filter, items_after))

        self.assertTrue(items_after, "Should maintain some items")
        self.assertFalse(items_after_filter, "Should have removed all filted ones")

    def test_delete_temp_item_bitstreams(self):
        """
        ! Indexing has to be cleared separately:
        > /dspace/bin/dspace cleanup
        in the docker container. (https://wiki.lyrasis.org/display/DSDOC6x/Command+Line+Operations)

        :return:
        """
        # Get all the bitstreams that I want to delete

        ### Does not seem we need to delete based on item?
        item_tmp_uuid = _get_temp_item(self.connector)

        bitstreams_item = self.connector.get_bitstreams(item_id=item_tmp_uuid)

        bitstreams = self.connector.get_bitstreams()

        l_inter = []
        for bitstream_i in bitstreams_item:
            if bitstream_i.uuid in map(lambda x: x.uuid, bitstreams):
                l_inter.append(bitstream_i)

        with self.subTest('Subset'):
            self.assertEqual(len(l_inter), len(bitstreams_item), 'Should be subset of all bitstreams')

        def f_filter(bitstream):

            # bitstream.parentObject is always None...

            return (bitstream.name is None)  # or ("2015 Annual Report" in item.name)

        for bitstream in filter(f_filter, bitstreams):
            self.connector.delete_bitstream(bitstream.uuid)

        # Delete bitstreams from temp item
        for bitstream in bitstreams_item:
            self.connector.delete_bitstream(bitstream.uuid)

        bitstreams_after = self.connector.get_bitstreams()
        bitstreams_after_filter = list(filter(f_filter, bitstreams_after))

        self.assertTrue(bitstreams_after, "Should maintain some bitstreams")
        self.assertFalse(bitstreams_after_filter, "Should have removed all filtered ones")

        return


class TestXMLResponse(unittest.TestCase):
    def test_str(self):
        response_content = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><item><link>/rest/items/ebb7f718-88f5-4083-a8fd-c915787c5015</link><expand>metadata</expand><expand>parentCollection</expand><expand>parentCollectionList</expand><expand>parentCommunityList</expand><expand>bitstreams</expand><expand>all</expand><handle>123456789/67</handle><name>Test 20201124 REST 2</name><type>item</type><UUID>ebb7f718-88f5-4083-a8fd-c915787c5015</UUID><archived>true</archived><lastModified>Mon May 31 10:02:24 UTC 2021</lastModified><withdrawn>false</withdrawn></item>'

        xml = XMLResponse.fromstring(response_content)

        s_xml = str(xml)

        def _concatenate_lines(s):
            return "".join(map(str.strip, s_xml.splitlines()))

        def _ingore_single_double_quotes(s):
            return s.replace("'", '"')

        self.assertEqual(
            _ingore_single_double_quotes(_concatenate_lines(s_xml)),
            _ingore_single_double_quotes(response_content.decode("UTF-8")),
        )


def _get_temp_collection(connector):
    collection0 = list(filter(lambda x: TestConnectorDSpaceRESTAddCollection.name in x.name, connector.get_collections()))[0]
    collection_id = collection0.uuid

    return collection_id


def _get_temp_item(connector, collection_id=None) -> str:
    if collection_id is None:
        collection_id = _get_temp_collection(connector)

    items = connector.get_items()

    name = 'temp item'

    f = filter(lambda item: item.name == name, items)

    for item in f:
        return item.uuid

    # Couldn't find item:
    item0 = ItemAdd(name=name)
    xml = connector.add_item(item0, collection_id)
    item0_uuid = xml.get_uuid()

    return item0_uuid
