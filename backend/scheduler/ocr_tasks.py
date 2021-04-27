import io
import logging

from documents.models import Page, Document, Overlay
from celery import shared_task
import documents.pagexml2geojson


logger = logging.getLogger(__name__)

@shared_task
def ocr_page(page_id):
    # POST to Pero OCR /post_processing_request
    # Creates the request

    # POST to Pero OCR /upload_image/{request_id}/{page_name}
    # Uploads image to the request

    # GET to Pero OCR /request_status/{request_id}
    # Checks the processing state of the request

    # GET to Pero OCR /download_results/{request_id}/{page_name}/{format}
    # Download results

    # Create Overlay object in Django

    # Save overlay XML to the object

    # Create Geojson overlay and save to the object

    page = Page.objects.get(pk=page_id)
    overlay = Overlay.objects.get(page=page)

    logger.info("OCR page: %s", page)
    logger.info("OCR pverlay: %s", overlay)

    overlay_file = overlay.file.file.read()
    geojson = documents.pagexml2geojson.main(io.BytesIO(overlay_file))

    logger.info(geojson)



