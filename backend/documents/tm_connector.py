import os
import abc

import requests

URL_BASE = os.environ['TM_URL']


class TmConnector(abc.ABC):

    def health_check(self):
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
        returns:
            list of found TM matches
        """
        pass

    def add_tu(self, key: str, langpair: str, seg: str, tra: str):
        """
        key: TM key, leave empty for public
        langpair: e.g.: en-nl
        seg: source segment
        tra: target segment
        """

    def delete_tu(self, key: str, langpair: str, seg: str, tra: str):
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

    def get_tu_amount(self, key: str, langpair: str) -> int:
        """
        key: TM key, leave empty for public
        langpair: e.g.: en-nl
        returns:
            total number of TUs for the given key and langpair
        """


class MouseTmConnector(TmConnector):
    URL_HEALTH = URL_BASE + '/admin/tminfo'
    URL_GET = URL_BASE + '/get'
    URL_SET = URL_BASE + '/set'
    URL_DELETE = URL_BASE + '/delete'
    URL_IMPORT_TMX = URL_BASE + '/tmx/import'
    URL_TU_AMOUNT = URL_BASE + '/tu/amount'

    def health_check(self):
        response = requests.get(self.URL_HEALTH)
        response.raise_for_status()
        return response

    def lookup_tu(self, concordance: bool, key: str, langpair: str, q: str):
        params = {
            'conc': concordance,
            'key': key,
            'langpair': langpair,
            'q': q
        }
        response = requests.get(self.URL_GET, params=params)
        response.raise_for_status()
        json_response = response.json()
        matches = json_response["matches"]
        return matches

    def add_tu(self, key: str, langpair: str, seg: str, tra: str):
        payload = {
            'key': key,
            'langpair': langpair,
            'seg': seg,
            'tra': tra
        }
        response = requests.post(self.URL_SET, data=payload)
        response.raise_for_status()
        return response

    def delete_tu(self, key: str, langpair: str, seg: str, tra: str):
        payload = {
            'key': key,
            'langpair': langpair,
            'seg': seg,
            'tra': tra
        }
        response = requests.post(self.URL_DELETE, data=payload)
        response.raise_for_status()
        return response

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
        return response

    def get_tu_amount(self, key: str, langpair: str) -> int:
        params = {
            'key': key,
            'langpair': langpair
        }
        response = requests.get(self.URL_TU_AMOUNT, params=params)
        response.raise_for_status()
        return int(response.content.decode('utf-8'))
