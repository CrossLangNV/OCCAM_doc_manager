"""
Connects to the XML translation API
"""

import abc
import os

import requests

URL_BASE = os.environ['CEF_ETRANSLATION_URL']


class TranslationConnector(abc.ABC):
    @abc.abstractmethod
    def translate_xml(self, file,
                      source: str,
                      target: str) -> bytes:
        """

        file: opened XML file
        source: language of the text
        target: language to translate to.
        returns:
            XML as bytestring (UTF-8)
        """
        pass


class CEFeTranslationConnector(TranslationConnector):
    URL_TRANSLATE_BLOCKING = URL_BASE + '/translate/xml/blocking'
    URL_TRANSLATE_POST = URL_BASE + '/translate/xml'
    URL_TRANSLATE_GET = URL_BASE + '/translate/xml/{xml_id}'

    def translate_xml(self,
                      file,
                      source,
                      target):
        files = {'file': file}

        headers = {'source': source,
                   'target': target}

        response = requests.post(self.URL_TRANSLATE_BLOCKING,
                                 headers=headers,
                                 files=files
                                 )

        if not response.ok:
            raise ConnectionError(f"Couldn't post request.\n{response.status_code}\n{response.content}")

        return response.content

    def translate_xml_post(self,
                           file,
                           source,
                           target
                           ) -> str:
        """
        Non-blocking, returns an ID
        """
        files = {'file': file}

        headers = {'source': source,
                   'target': target}

        response = requests.post(self.URL_TRANSLATE_POST,
                                 headers=headers,
                                 files=files
                                 )

        return response.json().get('id')

    def translate_xml_get(self,
                          xml_id: str) -> bytes:
        """
        Non-blocking, returns the translated XML
        """

        response = requests.get(self.URL_TRANSLATE_GET.format(xml_id=xml_id),
                                )

        return response.content
