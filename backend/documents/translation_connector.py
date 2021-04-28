"""
Connects to the XML translation API
"""

import requests

URL_TRANSLATE = 'http://192.168.105.41:9050/translate/xml/blocking'


def upload_file():
    raise NotImplementedError()
    return  # TODO


def translate_file(file,
                   source,
                   target):
    files = {'file': file}

    headers = {'source': source,
               'target': target}

    response = requests.post(URL_TRANSLATE,
                             headers=headers,
                             files=files
                             )

    if not response.ok:
        raise ConnectionError(f"Couldn't post request.\n{response.status_code}\n{response.content}")

    return response.content
