import urllib
import warnings
from types import SimpleNamespace
from typing import List, Union, Callable, Optional

import requests
from lxml import etree

from .models import Community, CommunityAdd, Collection, CollectionAdd, Item, ItemAdd, Bitstream

RESPONSE_TEST = "REST api is running."


class XMLResponse:
    def __init__(self, root_element: etree._Element):
        self.root = root_element
        self.tree = root_element.getroottree()

    @classmethod
    def fromstring(cls, string: bytes):
        return cls(etree.fromstring(string))

    def get_uuid(self):
        return self._get("UUID")

    def get_link(self):
        return self._get("link")

    def get_handle(self):
        return self._get("handle")

    def _get(self, key: str):
        return self.root.xpath(f"//{key}")[0].text

    def tostring(self):
        return etree.tostring(
            self.root, pretty_print=True, xml_declaration=True, standalone=True, encoding="UTF-8"
        ).decode("UTF-8")

    def print(self):
        return print(self.tostring())

    def __str__(self):
        return self.tostring()


class ConnectorDSpaceREST(requests.Session):
    """
    Connector to the DSpace REST API

    Make sure to close connection.
    Example:
    `
    with ConnectorDSpaceREST() as connector:
        connector.login(email, password)
    `

    """

    def __init__(self, url_dspace: str):
        """

        :param url_dspace: url to dspace server. E.g. 'http://test.dspace.com'
        """
        super().__init__()

        self.url_rest = url_dspace + "/rest"  # DSpace REST API
        response_test = requests.get(self.url_rest + "/test")

        if response_test.text != RESPONSE_TEST:
            warnings.warn(
                f"url_dspace is expected to be incorrect." f" {self.url_rest} should lead to the rest API.",
                UserWarning,
            )

        self.url_communities = self.url_rest + "/communities"
        self.url_collections = self.url_rest + "/collections"
        self.url_items = self.url_rest + "/items"
        self.url_bitstreams = self.url_rest + "/bitstreams"

    def login(self, email: str, password: str) -> str:
        """Needed when editing the elements (post, put, delete)

        You can also do a get request with:
        {url_rest}/login?email={email}&password={password}

        :param email:
        :param password:
        :return: a JSESSIONID as string
        """
        response = self.post(self.url_rest + "/login", data={"email": email, "password": password})

        JSESSIONID = response.cookies.get("JSESSIONID")
        return JSESSIONID

    def get_communities(self) -> List[SimpleNamespace]:
        data = self._get_all(self.url_communities)
        l = list(map(lambda d: Community(**d), data))

        return l

    def add_community(self, community: CommunityAdd):

        data = dict(vars(community))

        response = self.post(self.url_communities,
                             json=data,
                             )

        if response.ok:
            xml = XMLResponse.fromstring(response.content)
            return xml
        else:
            raise ConnectionError(response.content)

    def delete_community(self, community_uuid):

        url = self.url_communities + f"/{community_uuid}"
        response = self.delete(url)

        return response.ok

    def get_collections(self):

        data = self._get_all(self.url_collections)
        l = list(map(lambda d: Collection(**d), data))

        return l

    def add_collection(self, collection: CollectionAdd, community_id):
        url = self.url_communities + f"/{community_id}/collections"

        data = dict(vars(collection))

        response = self.post(url, json=data,
                             )

        if response.ok:
            xml = XMLResponse.fromstring(response.content)
            return xml
        else:
            raise ConnectionError(response.content)

    def delete_collection(self, collection_uuid):

        url = self.url_collections + f"/{collection_uuid}"
        response = self.delete(url)

        return response.ok

    def get_items(
            self,
    ):

        data = self._get_all(self.url_items)

        l = list(map(lambda d: Item(**d), data))

        return l

    def add_item(self, item: ItemAdd, collection_id: int, metadata: dict) -> XMLResponse:

        url = self.url_collections + f"/{collection_id}/items"

        dcm = DCMetadata(title=item.name, description=metadata["description"],
                         contributor=metadata["contributor"],
                         creator=metadata["creator"],
                         subject=metadata["subject"],
                         publisher=metadata["publisher"],
                         date=metadata["date"],
                         type=metadata["type"],
                         format=metadata["format"],
                         identifier=metadata["identifier"],
                         source=metadata["source"],
                         language=metadata["language"],
                         relation=metadata["relation"],
                         rights=metadata["rights"])

        metadata = dcm.get_metadata()

        data = {
            'name': item.name,
            "metadata": metadata
        }

        response = self.post(url, json=data,
                             )

        if response.ok:
            xml = XMLResponse.fromstring(response.content)
        else:
            raise ConnectionError(response.content)

        return xml

    def delete_item(self, uuid):

        url = self.url_items + f"/{uuid}"
        self.delete(url)

    def get_bitstreams(self,
                       item_id: str = None):
        """

        :param item_id: (Optional)
        :return:
        """

        if item_id is None:
            data = self._get_all(self.url_bitstreams)
        else:
            data = self._get_all(self.url_items + f'/{item_id}/bitstreams')

        l = list(map(lambda d: Bitstream(**d), data))

        return l

    def add_bitstream(self,
                      file,
                      basename: str,
                      item_id: str,
                      description: str = None,
                      groupId: int = None,
                      year: int = None,
                      month: int = None,
                      day: int = None,
                      ):
        """

        Example code:
        `
        description = 'this a description'
        with open(filename, 'rb') as file:
            r = self.connector.add_bitstream(file,
                                             filename,
                                             'aaa-bbb-ccc',
                                             description=description)
        `

        Format and mimeType are found automatically

        :param file:
        :param basename:
        :param item_id:
        :param description: (Optional)
        :param groupId: (Optional) Id of group to set item resource policy to.'
        :param year: (Optional) Year to set embargo date to
        :param month: (Optional) Month to set embargo date to
        :param day: (Optional) Day of month to set embargo date to
        :return:
        """

        url = self.url_items + f"/{item_id}/bitstreams?name={urllib.parse.quote(basename)}"

        if description:
            url += f"&description={urllib.parse.quote(description)}"

        if groupId:
            url += f"&groupID={groupId:d}"

        # Embargo date
        if year:
            url += f"&year={year:d}"
            if month:
                url += f"&month={month:d}"
                if day:
                    url += f"&day={day:d}"

        # https://stackoverflow.com/questions/16145116/python-requests-post-data-from-a-file/16145232#16145232
        # https://stackoverflow.com/questions/43580/how-to-find-the-mime-type-of-a-file-in-python
        # headers = {"content-type" : "multipart/form-data"}
        response = self.post(url,
                             data=file,
                             # headers=headers
                             )

        assert response.ok, 'Failed to uplaod file.' + f'\n{response.content}\n{response.status_code}'

        return response.content

    def delete_bitstream(self, uuid):

        url = self.url_bitstreams + f"/{uuid}"
        self.delete(url)

    def _get_all(self, url, limit=100):
        data = []
        i = 0

        while True:
            offset = i * limit
            # Default value of limit is 100
            response = self.get(url + f"?offset={offset:d}&limit={limit:d}")

            if not response.ok:
                raise ConnectionError(response.content)

            data_i = response.json()

            if len(data_i):
                data.extend(data_i)

            if len(data_i) < limit:
                break

            i += 1

        return data


class DCMetadata:
    """
    Metadata elements: https://ndlib.github.io/metadata_application_profile/elements/index.html
    """

    def __init__(
            self,
            # Required
            title: str,
            # Not required
            description: Optional[str],
            contributor: Union[list, str] = None,
            abstract: Union[list, str] = None,
            creator: Union[list, str] = None,
            subject: Union[list, str] = None,
            publisher: Union[list, str] = None,
            date: Union[list, str] = None,
            type: Union[list, str] = None,
            format: Union[list, str] = None,
            identifier: Union[list, str] = None,
            source: Union[list, str] = None,
            language: Union[list, str] = None,
            relation: Union[list, str] = None,
            rights: Union[list, str] = None,
    ):

        self.title = title

        self.description = description
        self.contributor = contributor
        self.abstract = abstract
        self.creator = creator
        self.subject = subject
        self.publisher = publisher
        self.date = date
        self.type = type
        self.format = format
        self.identifier = identifier
        self.source = source
        self.language = language
        self.relation = relation
        self.rights = rights

    def get_metadata(self):

        metadata = []

        def add_title(title):
            metadata.append({"key": "dc.title", "value": title})
            # metadata.append({"key": "dcterms.title", "value": title})

        def add_description(description):
            metadata.append({"key": "dc.description", "value": description})

        def add_contributor(contributor):
            metadata.append({"key": "dc.contributor.author", "value": contributor})

        def add_abstract(abstract):
            metadata.append({"key": "dc.abstract", "value": abstract})

        def add_creator(creator):
            metadata.append({"key": "dc.creator", "value": creator})

        def add_subject(subject):
            metadata.append({"key": "dc.subject", "value": subject})

        def add_publisher(publisher):
            metadata.append({"key": "dc.publisher", "value": publisher})

        def add_date(date):
            metadata.append({"key": "dc.date", "value": date})

        def add_type(type):
            metadata.append({"key": "dc.type", "value": type})

        def add_format(format):
            metadata.append({"key": "dc.format", "value": format})

        def add_identifier(identifier):
            metadata.append({"key": "dc.identifier", "value": identifier})

        def add_source(source):
            metadata.append({"key": "dc.source", "value": source})

        def add_language(language):
            metadata.append({"key": "dc.language", "value": language})

        def add_relation(relation):
            metadata.append({"key": "dc.relation", "value": relation})

        def add_rights(rights):
            metadata.append({"key": "dc.rights", "value": rights})

        def meta_factory(el, add_i: Callable[[str], None]):
            if el is None:
                return

            l = el if isinstance(el, (list, tuple)) else [el]
            for el_i in l:
                add_i(el_i)

        meta_factory(self.title, add_title)
        meta_factory(self.description, add_description)
        meta_factory(self.contributor, add_contributor)
        meta_factory(self.abstract, add_abstract)
        meta_factory(self.creator, add_creator)
        meta_factory(self.subject, add_subject)
        meta_factory(self.publisher, add_publisher)
        meta_factory(self.date, add_date)
        meta_factory(self.type, add_type)
        meta_factory(self.format, add_format)
        meta_factory(self.identifier, add_identifier)
        meta_factory(self.source, add_source)
        meta_factory(self.language, add_language)
        meta_factory(self.relation, add_relation)
        meta_factory(self.rights, add_rights)

        return metadata
