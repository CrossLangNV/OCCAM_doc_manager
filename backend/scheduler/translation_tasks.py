import io
import logging
import os

from celery import shared_task
from django.contrib.auth.models import User

from activitylogs.models import ActivityLog, ActivityLogType, ActivityLogState
from documents.models import Overlay
from documents.translation_connector import CEFeTranslationConnector

logger = logging.getLogger(__name__)


@shared_task
def translate_overlay(overlay_id, target, user=None):
    """
    overlay_id : id from Overlay model object
    source: abbreviation of the language of the text
    target: abbreviation of language to translate to
    """
    overlay = Overlay.objects.get(pk=overlay_id)

    source = overlay.source_lang
    logger.info("Translating page: %s", overlay)
    logger.info("Source language: %s", source)
    logger.info("Target language: %s", target)

    activity_log = ActivityLog.objects.create(
        overlay=overlay,
        page=overlay.page,
        type=ActivityLogType.TRANSLATION,
        state=ActivityLogState.PROCESSING
    )

    if user:
        user_obj = User.objects.get(email=user)
        activity_log.user = user_obj
        activity_log.save()

    logger.info("Created activity log")

    conn = CEFeTranslationConnector()

    # Blocking translation request
    try:
        with overlay.get_file().open("rb") as f:
            xml_trans = conn.translate_xml(f, source, target)

            # Save to translation in overlay object
            with io.BytesIO(xml_trans) as f:
                basename, ext = os.path.splitext(overlay.get_file().name)
                name = basename + f"_{source}_{target}" + ext
                f.name = name

                overlay.update_transl_xml(f, target=target)

            activity_log.state = ActivityLogState.SUCCESS
            activity_log.save()

            return True
    except Exception as e:
        print(e)
        activity_log.state = ActivityLogState.FAILED
        activity_log.save()
