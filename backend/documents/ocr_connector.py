import os
import requests

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']


def get_request_id(page_id: str):
    data = {
        "engine": 1,
        "images": {
            page_id: None
        }
    }

    response_request = requests.post('https://pero-ocr.fit.vutbr.cz/api/post_processing_request',
                                     json=data,
                                     headers={'api-key': API_KEY_PERO_OCR,
                                              'Content-Type': 'application/json',
                                              'accept': 'application/json'
                                              },
                                     )

    if not response_request.ok:
        raise Exception({'status_code': response_request.status_code,
                         'content': response_request.content})
    request_id = response_request.json()['request_id']
    return request_id


def upload_file(file,
                request_id: str,
                page_id: str,
                ):
    """

    Example:
        >> with page.file.open() as file:
        >>    upload_file(file,
        >>                request_id=request_id,
        >>                page_id=page_id
        >>                )
    """

    files = {'file': file}

    response_upload_image = requests.post(f'https://pero-ocr.fit.vutbr.cz/api/upload_image/{request_id}/{page_id}',
                                          files=files,
                                          headers={'api-key': API_KEY_PERO_OCR,
                                                   },
                                          )

    if not response_upload_image.ok:
        raise Exception({'status_code': response_upload_image.status_code,
                         'content': response_upload_image.content})


def check_state(request_id: str, page_id: str) -> bool:
    """
    Check state of OCR request.

    return: True if finished, else False
    """
    response_status = requests.get(
        f'https://pero-ocr.fit.vutbr.cz/api/request_status/{request_id}',
        headers={'api-key': API_KEY_PERO_OCR,
                 },
    )

    state = response_status.json()['request_status'][page_id]['state']

    return not (state in ('WAITING', 'PROCESSING'))


def get_result(request_id,
               page_id,
               result_format='page'  # alto, page, txt
               ):
    """
    Returns the Overlay xml as bytestring
    """

    response_download_results = requests.get(
        f'https://pero-ocr.fit.vutbr.cz/api/download_results/{request_id}/{page_id}/{result_format}',
        headers={'api-key': API_KEY_PERO_OCR,
                 },
    )

    if not response_download_results.ok:
        raise Exception({'status_code': response_download_results.status_code,
                         'content': response_download_results.content})

    return response_download_results.content
