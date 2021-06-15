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


class MouseTmConnector(TmConnector):
    URL_HEALTH = URL_BASE + '/admin/tminfo'

    def health_check(self) -> bytes:
        response = requests.get(self.URL_HEALTH)
        response.raise_for_status()
        return response.content
