import io
import logging
import time
from django.core.files import File
import os
from documents.models import Page, Document, Overlay
from celery import shared_task
from documents import pagexml2geojson
from documents.ocr_connector import get_request_id, check_state, get_result, upload_file
import json

logger = logging.getLogger(__name__)


@shared_task
def ocr_page(page_id):
    page = Page.objects.get(pk=page_id)

    logger.info("Started OCR for page: %s", page)

    page_name = page.file.name

    logger.info("Page name: %s", page_name)

    # POST to Pero OCR /post_processing_request
    # Creates the request
    request_id = get_request_id(page_name)
    logger.info("Sent request to per ocr: %s", request_id)

    # POST to Pero OCR /upload_image/{request_id}/{page_name}
    # Uploads image to the request
    with page.file.open() as file:
        upload_file(file,
                    request_id=request_id,
                    page_name=page_name,
                    )

    # GET to Pero OCR /request_status/{request_id}
    # Checks the processing state of the request
    # Check if finished!

    logger.info("Waiting for document to be processed....")
    while True:
        if check_state(request_id,
                       page_name):
            break
        else:  # 'PROCESSED'
            time.sleep(1)
    logger.info("Document is processed!")

    # GET to Pero OCR /download_results/{request_id}/{page_name}/{format}
    # Download results
    overlay_xml = get_result(request_id,
                             page_name)
    logger.info("OCR overlay xml: %s", overlay_xml)

    # Create Overlay object in Djang
    # TODO should we update if already exists?
    overlay = Overlay.objects.create(page=page)
    logger.info("OCR overlay: %s", overlay)

    basename, _ = os.path.splitext(page_name)

    # Save overlay XML to the object
    with io.BytesIO(overlay_xml) as f:
        f.name = basename + '.xml'
        logger.info("f name: %s", f.name)
        overlay.update_xml(f)

    # Create Geojson overlay and save to the object
    geojson = pagexml2geojson.main(io.BytesIO(overlay_xml))
    logger.info(geojson)

    with File(io.BytesIO(json.dumps(geojson).encode('utf-8'))) as django_file:
        overlay.geojson.save(basename + '.geojson', django_file)
        overlay.save()
