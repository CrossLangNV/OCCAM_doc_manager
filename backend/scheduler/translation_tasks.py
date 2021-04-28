import io
import logging
import os

from django.core.files import File

from celery import shared_task
from documents.models import Overlay
from documents.translation_connector import CEFeTranslationConnector

logger = logging.getLogger(__name__)


@shared_task
def translate_overlay(overlay_id,
                      source,
                      target):
    """
    overlay_id : id from Overlay model object
    source: abbreviation of the language of the text
    target: abbreviation of language to translate to
    """
    overlay = Overlay.objects.get(pk=overlay_id)

    logger.info("Translating page: %s", overlay)
    logger.info("Source language: %s", source)
    logger.info("Target language: %s", target)

    conn = CEFeTranslationConnector()

    # POST to XML Translation /translate/xml
    # Send a translation request and get the ID to poll to
    with overlay.get_file().open('rb') as f:
        xml_trans = conn.translate_xml(f,
                                       source,
                                       target)

    # GET to XML Translation /translate/xml/{xml_id}
    # Keep polling until it's finished.

    # Save to translation in overlay object
    with io.BytesIO(xml_trans) as f:
        basename, ext = os.path.splitext(overlay.get_file().name)

        with File(f) as django_file:
            overlay.translation_file.save(name=basename + f'_{source}_{target}' + ext,
                                          content=django_file)
            overlay.save()

    return True
