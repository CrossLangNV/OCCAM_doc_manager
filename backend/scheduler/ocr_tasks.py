import io
import logging
import os
import time

from celery import shared_task

from activitylogs.models import ActivityLog, ActivityLogType
from documents.models import Page, Overlay
from documents.ocr_connector import get_request_id, check_state, get_result, upload_file

logger = logging.getLogger(__name__)


@shared_task
def ocr_page(page_id):
    page = Page.objects.get(pk=page_id)

    logger.info("Started OCR for page: %s", page)

    page_id = str(page.id)
    basename, _ = os.path.splitext(page.file.name)

    logger.info("Page name: %s", basename)

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

    activity_log = ActivityLog.objects.create(page=page,
                                              type=ActivityLogType.OCR)
    logger.info("Created activity log")

    logger.info("Waiting for document to be processed....")
    while True:
        if check_state(request_id,
                       page_id, activity_log):
            break
        else:  # 'PROCESSED'
            time.sleep(1)
    logger.info("Document is processed!")

    # GET to Pero OCR /download_results/{request_id}/{page_id}/{format}
    # Download results
    overlay_xml = get_result(request_id,
                             page_id)
    logger.info("OCR overlay xml: %s", overlay_xml)

    # Create Overlay object in Djang
    # TODO should we update if already exists?
    # TODO GEt language from classifier
    source_lang = "EN"
    overlay = Overlay.objects.create(page=page, source_lang=source_lang)
    logger.info("OCR overlay: %s", overlay)

    # Save overlay XML to the object
    with io.BytesIO(overlay_xml) as f:
        f.name = basename + '.xml'
        logger.info("f name: %s", f.name)
        overlay.update_xml(f)
