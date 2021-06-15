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


class MouseTmConnector(TmConnector):
    URL_HEALTH = URL_BASE + '/admin/tminfo'
    URL_GET = URL_BASE + '/get'
    URL_SET = URL_BASE + '/set'

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
