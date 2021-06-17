import os
import abc

import requests

URL_BASE = os.environ['TM_URL']


class TmConnector(abc.ABC):

    def health_check(self) -> bytes:
        """
        returns:
            any response to check if TM API is up and running
        """
        pass

    def lookup_tu(self, concordance: bool, key: str, langpair: str, q: str):
        """
        concordance: if true, include partial matches
        key: TM key, leave empty for public
        langpair: e.g.: en-nl
        q: the term/phrase for which to look for in the TM
        """
        pass

    def add_tu(self, key: str, langpair: str, seg: str, tra: str):
        """
        key: TM key, leave empty for public
        langpair: e.g.: en-nl
        seg: source segment
        tra: target segment
        """

    def import_tmx(self, key: str, name: str, tmx):
        """
        key: TM key, leave empty for public
        name: name of tmx file (optional)
        tmx: tmx file to upload
        """


class MouseTmConnector(TmConnector):
    URL_HEALTH = URL_BASE + '/admin/tminfo'
    URL_GET = URL_BASE + '/get'
    URL_SET = URL_BASE + '/set'
    URL_IMPORT_TMX = URL_BASE + '/tmx/import'

    def health_check(self) -> bytes:
        response = requests.get(self.URL_HEALTH)
        response.raise_for_status()
        return response.content

    def lookup_tu(self, concordance: bool, key: str, langpair: str, q: str):
        params = {
            'conc': concordance,
            'key': key,
            'langpair': langpair,
            'q': q
        }
        response = requests.get(self.URL_GET, params=params)
        response.raise_for_status()
        return response.content

    def add_tu(self, key: str, langpair: str, seg: str, tra: str):
        payload = {
            'key': key,
            'langpair': langpair,
            'seg': seg,
            'tra': tra
        }
        response = requests.post(self.URL_SET, data=payload)
        response.raise_for_status()
        return response.content

    def import_tmx(self, key: str, name: str, tmx):
        data = {
            'key': key,
            'name': name,
        }
        files = {
            'tmx': tmx
        }
        response = requests.post(self.URL_IMPORT_TMX, data=data, files=files)
        response.raise_for_status()
        return response.content
