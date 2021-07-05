import io
import logging
import os
import time

import requests
from celery import shared_task
from django.contrib.auth.models import User
from langdetect import detect
from xml_orm.orm import PageXML

from activitylogs.models import ActivityLog, ActivityLogType, ActivityLogState
from documents.models import Page, Overlay, Label
from documents.ocr_connector import get_request_id, check_state, get_result, upload_file

logger = logging.getLogger(__name__)

DOCUMENT_CLASSIFIER_URL = os.environ["DOCUMENT_CLASSIFIER_URL"]


@shared_task
def ocr_page_pipeline(page_id: Page.id,
                      user=None,
                      activity_log: ActivityLog = None):
    page = Page.objects.get(pk=page_id)
    logger.info("Started OCR for page: %s", page)

    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user=user)

    classify_document(page)
    activity_log.state = ActivityLogState.CLASSIFIED
    activity_log.save()
    logger.info("Classified page")

    overlay_xml = get_overlay_from_pero_ocr(page,
                                            activity_log=activity_log)

    create_overlay_with_language(page, overlay_xml, activity_log=activity_log)


@shared_task
def upload_overlay_pipeline(page_id,
                            user=None,
                            activity_log: ActivityLog = None):
    logger.info("Started processing for a manually uploaded document")

    logger.info("page: %s", page_id)

    page = Page.objects.get(pk=page_id)
    logger.info("Started upload for page: %s", page)

    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user=user)

    classify_document(page)
    activity_log.state = ActivityLogState.CLASSIFIED
    activity_log.save()
    logger.info("Classified page")

    # overlay = Overlay.objects.filter(page=page).latest("created_at")
    # logger.info("overlay: ", overlay)
    # with overlay.file.open('rb') as f:
    #     overlay_xml = f.read()
    # create_overlay_with_language(page, overlay_xml, activity_log=activity_log)


def get_activity_log(page: Page,
                     user: User.email = None):
    activity_log = ActivityLog.objects.create(page=page,
                                              type=ActivityLogType.OCR)
    if user:
        user_obj = User.objects.get(email=user)
        activity_log.user = user_obj
        activity_log.save()

    return activity_log


def get_overlay_from_pero_ocr(page: Page,
                              user=None,
                              activity_log: ActivityLog = None):
    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user=user)

    page_id = page.id

    # POST to Pero OCR /post_processing_request
    # Creates the request
    request_id = get_request_id(page_id)
    logger.info("Sent request to per ocr: %s", request_id)

    # POST to Pero OCR /upload_image/{request_id}/{page_id}
    # Uploads image to the request
    with page.file.open() as file:
        upload_file(file,
                    request_id=request_id,
                    page_id=page_id,
                    )

    # GET to Pero OCR /request_status/{request_id}
    # Checks the processing state of the request
    # Check if finished!

    logger.info("Waiting for document to be processed....")
    while True:
        if check_state(request_id,
                       page_id, activity_log):
            logger.info("Document is processed!")
            break
        else:  # 'PROCESSED'
            time.sleep(1)

    # GET to Pero OCR /download_results/{request_id}/{page_id}/{format}
    # Download results
    overlay_xml = get_result(request_id,
                             page_id)
    logger.info("OCR overlay xml: %s", overlay_xml)

    return overlay_xml


def create_overlay_with_language(page: Page, overlay_xml: bytes,
                                 user=None,
                                 activity_log=None):
    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user=user)

    page_id = page.id

    basename, _ = os.path.splitext(page.file.name)
    logger.info("Page name: %s", basename)

    # Create Overlay object in Django
    # TODO perhaps no need to first convert to file
    try:
        with io.BytesIO(overlay_xml) as f:
            source_lang = xml_lang_detect(f)
    except Exception as e:
        activity_log.state = ActivityLogState.FAILED
        print("Langdetect failed for page id: ", page_id)

    overlay, _ = Overlay.objects.update_or_create(page=page,
                                                  defaults={'source_lang': source_lang}
                                                  )
    logger.info("OCR overlay: %s", overlay)

    activity_log.overlay = overlay
    activity_log.save()

    # Save overlay XML to the object
    with io.BytesIO(overlay_xml) as f:
        f.name = basename + '.xml'
        logger.info("f name: %s", f.name)
        overlay.update_xml(f)


def xml_lang_detect(xml_file):
    a = PageXML(xml_file)

    l_reg = list(filter(lambda s: s, a.get_regions_text()))
    s_all = ' '.join(l_reg)

    lang = detect(s_all).upper()

    # l = list(map(detect, l_reg))

    return lang


def get_document_classification(page):
    headers = {
        "model-id": "1",
    }

    f = page.file
    files = {'file': f}

    r = requests.post(DOCUMENT_CLASSIFIER_URL, headers=headers, files=files)

    res = r.json()

    print("classification result: ", res)

    return res


def classify_document(page):
    # POST to Document Classifier
    classification_results = get_document_classification(page)

    if classification_results:
        for label, value in classification_results.items():
            Label.objects.update_or_create(page=page, name=label, defaults={'name': label, 'value': value})
            print("created label: ", label)
