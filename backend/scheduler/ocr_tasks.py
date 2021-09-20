import io
import os
import time

from celery import shared_task
from django.contrib.auth.models import User
from langdetect import detect
from xml_orm.orm import PageXML

from activitylogs.models import ActivityLog, ActivityLogState
from documents.models import Page, Overlay, LayoutAnalysisModel
from documents.ocr_connector import PeroOcrWebApiConnector, LocalOcrConnector
from documents.ocr_engines import get_PERO_OCR_engine_id
from scheduler.tasks import logger, get_activity_log


@shared_task
def ocr_page_pipeline(page_pk: Page.pk,
                      engine_pk: LayoutAnalysisModel.pk,
                      user_pk: User.pk = None,
                      activity_log: ActivityLog = None):
    page = Page.objects.get(pk=page_pk)
    logger.info("Started OCR for page: %s", page)

    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user_pk=user_pk)

    overlay_xml = get_overlay_from_pero_ocr(page,
                                            int(engine_pk),
                                            activity_log=activity_log)

    create_overlay_with_language(page, overlay_xml, activity_log=activity_log)


def get_overlay_from_pero_ocr(page: Page,
                              engine_pk: LayoutAnalysisModel.pk,
                              user_pk: User.pk = None,
                              activity_log: ActivityLog = None) -> bytes:
    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user_pk=user_pk)

    # POST to Pero OCR /post_processing_request
    # Creates the request

    layout_analysis_model = LayoutAnalysisModel.objects.get(pk=engine_pk)
    logger.info("Used engine: %s", layout_analysis_model)

    # Local engine
    if layout_analysis_model.config.get('link') == 'LOCAL_PERO':
        # TODO actually add the BRIS model!
        connector = LocalOcrConnector(activity_log=activity_log)

        logger.info("Sent request to Pero OCR: local")

        with page.file.open() as file:
            overlay_xml = connector.ocr_image(file)

    else:
        page_pk = str(page.pk)
        pero_engine_id = get_PERO_OCR_engine_id(layout_analysis_model)

        connector = PeroOcrWebApiConnector()

        request_id = connector.get_request_id(page_pk,
                                              pero_engine_id=int(pero_engine_id))
        logger.info("Sent request to Pero OCR: %s", request_id)

        # POST to Pero OCR /upload_image/{request_id}/{page_pk}
        # Uploads image to the request
        with page.file.open() as file:
            connector.upload_file(file,
                                  request_id=request_id,
                                  page_pk=page_pk,
                                  )

        # GET to Pero OCR /request_status/{request_id}
        # Checks the processing state of the request
        # Check if finished!

        logger.info("Waiting for document to be processed....")
        while True:
            if connector.check_state(request_id,
                                     page_pk, activity_log):
                logger.info("Document is processed!")
                break
            else:  # 'PROCESSED'
                time.sleep(1)

        # GET to Pero OCR /download_results/{request_id}/{page_pk}/{format}
        # Download results
        overlay_xml = connector.get_result(request_id,
                                           page_pk)
        logger.info("OCR overlay xml: %s", overlay_xml)

    return overlay_xml


def create_overlay_with_language(page: Page, overlay_xml: bytes,
                                 user_pk=None,
                                 activity_log=None):
    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user_pk=user_pk)

    page_pk = page.pk

    basename, _ = os.path.splitext(page.file.name)
    logger.info("Page name: %s", basename)

    # Create Overlay object in Django
    # TODO perhaps no need to first convert to file
    try:
        with io.BytesIO(overlay_xml) as f:
            source_lang = xml_lang_detect(f)
    except Exception as e:
        activity_log.state = ActivityLogState.FAILED
        print("Langdetect failed for page id: ", page_pk)
    # Create Overlay object in Django
    # TODO should we update if already exists?

    try:
        # TODO perhaps no need to first convert to file
        with io.BytesIO(overlay_xml) as f:
            source_lang = xml_lang_detect(f)
    except Exception as e:
        activity_log.state = ActivityLogState.FAILED
        print("Langdetect failed for page id: ", page_pk)

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


def xml_lang_detect(xml_file) -> str:
    a = PageXML(xml_file)

    l_reg = list(filter(lambda s: s, a.get_regions_text()))

    # Join all the pieces of text
    s_all = ' '.join(l_reg)
    # Convert to uppercase language representation, e.g. EN.
    lang = detect(s_all).upper()

    return lang
