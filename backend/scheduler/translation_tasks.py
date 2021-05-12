import io
import logging
import os

from celery import shared_task
from documents.models import Overlay, Geojson
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

    # Blocking translation request
    with overlay.get_file().open('rb') as f:
        xml_trans = conn.translate_xml(f,
                                       source,
                                       target)

    # Save to translation in overlay object
    with io.BytesIO(xml_trans) as f:
        basename, ext = os.path.splitext(overlay.get_file().name)
        name = basename + f'_{source}_{target}' + ext
        f.name = name

        overlay.update_transl_xml(f)

    geojson = Geojson.objects.create(overlay=overlay,
                                     original=False,
                                     lang=target,
                                     source_lang=source,  # Optional
                                     )

    # Can't combine since the previous update will close the file.
    with io.BytesIO(xml_trans) as f:
        basename, ext = os.path.splitext(overlay.get_file().name)
        name = basename + f'_{source}_{target}' + ext
        f.name = name
        geojson.update_file(f)

    return True
