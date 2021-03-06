"""
Connector methods to PERO-OCR's API.
"""
import abc
import logging
import os

import requests

from activitylogs.models import ActivityLogState, ActivityLog

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']
LOCAL_PERO = os.environ['LOCAL_PERO']

PERO_OCR_API = 'https://pero-ocr.fit.vutbr.cz/api/'

KEY_ENGINES = 'engines'
KEY_STATUS = 'status'
KEY_DESCRIPTION = 'description'
VALUE_STATUS = 'success'

KEY_ENGINE_ID = 'id'
KEY_MODELS = 'models'
KEY_MODEL_ID = 'id'
KEY_MODEL_NAME = 'name'

logger = logging.getLogger(__name__)


class OcrConnector(abc.ABC):
    pass


class PeroOcrWebApiConnector(OcrConnector):

    def get_request_id(self,
                       page_pk: str,
                       pero_engine_id: int,
                       b_info: bool = True) -> str:
        """

        Args:
            page_pk:
            pero_engine_id:
                As defined by the PERO-OCR API engines.
                Attention! Not te be confused with LayoutAnalysisModel.pk.
            b_info: (bool) set to True to print info messages.

        Returns:

        """

        data = {
            "engine": pero_engine_id,
            "images": {
                page_pk: None
            }
        }

        if b_info:
            engines = self.get_pero_web_engines()
            engine_name = next(filter(lambda engine_name: engines.get(engine_name).get(KEY_ENGINE_ID) == pero_engine_id,
                                      engines))
            logger.info("Using OCR engine: %s", engine_name)
            print("Using OCR engine: %s" % engine_name)

        response_request = requests.post(PERO_OCR_API + 'post_processing_request',
                                         json=data,
                                         headers={'api-key': API_KEY_PERO_OCR,
                                                  'Content-Type': 'application/json',
                                                  'accept': 'application/json'
                                                  },
                                         )

        if not response_request.ok:
            _raise_response(response_request)

        request_id = response_request.json()['request_id']

        if b_info:
            status = self.get_request_status(request_id)
            # logger.info("Request status: %s", status)
            print("Request status: %s" % status)
            logger.info("Request status 2: %s" % status)

        return request_id

    def upload_file(self,
                    file,
                    request_id: str,
                    page_pk: str,
                    ) -> None:
        """

        Example:
            >> with page.file.open() as file:
            >>    upload_file(file,
            >>                request_id=request_id,
            >>                page_pk=page_pk
            >>                )
        """

        files = {'file': file}

        response_upload_image = requests.post(f'https://pero-ocr.fit.vutbr.cz/api/upload_image/{request_id}/{page_pk}',
                                              files=files,
                                              headers={'api-key': API_KEY_PERO_OCR,
                                                       },
                                              )

        if not response_upload_image.ok:
            _raise_response(response_upload_image)

    def check_state(self,
                    request_id: str, page_pk: str, activity_log) -> bool:
        """
        Check state of OCR request.

        return: True if finished, else False
        """

        response_status = self.get_request_status(request_id)
        state = response_status['request_status'][page_pk]['state']

        if state == "PROCESSED":
            activity_log.state = ActivityLogState.SUCCESS
            activity_log.save()
        else:
            activity_log.state = ActivityLogState.PROCESSING
            activity_log.save()

        activity_log.save()

        return not (state in ('WAITING', 'PROCESSING'))

    def get_result(self,
                   request_id,
                   page_pk,
                   result_format='page'  # alto, page, txt
                   ) -> bytes:
        """
        Returns the Overlay xml as bytestring
        """

        response_download_results = requests.get(
            f'https://pero-ocr.fit.vutbr.cz/api/download_results/{request_id}/{page_pk}/{result_format}',
            headers={'api-key': API_KEY_PERO_OCR,
                     },
        )

        if not response_download_results.ok:
            _raise_response(response_download_results)

        return response_download_results.content

    def get_request_status(self, request_id) -> dict:
        """

        Args:
            request_id: The ID as returned by :func:`~get_request_id`

        Returns:

        """

        response_status = requests.get(
            PERO_OCR_API + f'request_status/{request_id}',
            headers={'api-key': API_KEY_PERO_OCR,
                     },
        )

        return response_status.json()

    def get_pero_web_engines(self) -> dict:
        """
        info about the OCR engines in PERO-OCR. Engine includes layout analysis + OCR.

        Returns a dictionary: {name_engine : info_engine, ...}.
        info_engine contains another dictionary with additional info.
        """

        response_engines = requests.get('https://pero-ocr.fit.vutbr.cz/api/get_engines',
                                        headers={'api-key': API_KEY_PERO_OCR})

        if not response_engines.ok:
            content = {'message': 'PERO-OCR engines not found.',
                       'status code': response_engines.status_code,
                       'content': response_engines.content,
                       }
            raise ConnectionError(content)

        b = 0
        if b:
            model_czech = response_engines.json()['engines']['czech_old_printed']
            model_layout = next(filter(lambda x: 'layout' in x['name'], model_czech['models']))
            model_ocr = next(filter(lambda x: 'layout' not in x['name'], model_czech['models']))

        if not response_engines.ok:
            _raise_response(response_engines)

        d_response = response_engines.json()

        if VALUE_STATUS not in d_response.get(KEY_STATUS):
            _raise_response(response_engines,
                            message='No success found')

        return d_response[KEY_ENGINES]


class LocalOcrConnector(OcrConnector):
    def __init__(self,
                 activity_log: ActivityLog = None):
        self.activity_log = activity_log

    def ocr_image(self,
                  file,
                  ) -> bytes:
        """
        OCRs a page and return the overlay as a page xml bytestring.

        args:
            file: an image file to be OCR'ed

        Example:
            >> with page.file.open() as file:
            >>    overlay_xml = ocr_image(file)
        """

        files = {'image': file}

        if self.activity_log:
            self.activity_log.state = ActivityLogState.PROCESSING
            self.activity_log.save()

        response_ocr_image = requests.post(f'{os.path.join(LOCAL_PERO, "ocr/")}',
                                           files=files,
                                           )

        if not response_ocr_image.ok:
            if self.activity_log:
                self.activity_log.state = ActivityLogState.FAILED
                self.activity_log.save()

            _raise_response(response_ocr_image)

        if self.activity_log:
            self.activity_log.state = ActivityLogState.SUCCESS
            self.activity_log.save()

        return response_ocr_image.json()['xml'].encode()


def _raise_response(
        response,
        message: str = None):
    """
    Raises an exception with information about the response.

    Args:
        response: Response from a request
        message: (Optional) To add a message to the dictionary that is raised with the exception.

    Returns:
        None
    """

    feedback = {'status_code': response.status_code,
                'content': response.content,
                'text': response.text
                }

    if message is not None:
        feedback['message'] = message

    # Try to add json, if available
    try:
        feedback['json'] = response.json()
    except Exception:
        pass

    raise Exception(feedback)
