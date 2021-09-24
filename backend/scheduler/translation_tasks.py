import io
import logging
import os

from django.contrib.auth.models import User

from activitylogs.models import ActivityLog, ActivityLogType, ActivityLogState
from celery import shared_task
from documents.models import Overlay, Document
from documents.translation_connector import CEFeTranslationConnector

logger = logging.getLogger(__name__)


@shared_task
def translate_all_pages(document_id, target_language, use_tm, user_email):
    logger.info("Translating all pages:")
    logger.info("document_id: %s", document_id)
    logger.info("target_language: %s", target_language)
    logger.info("use_tm: %s", use_tm)
    logger.info("user_email: %s", user_email)

    user_pk = User.objects.get(email=user_email).pk
    document = Document.objects.get(id=document_id)

    for page in document.document_page.all():
        print("page: ", page)

        overlay = page.page_overlay.last()
        print("overlay: ", overlay)

        translate_overlay.delay(overlay.pk, target_language, use_tm, user_pk)



@shared_task
def translate_overlay(overlay_pk: Overlay.pk, target: str, use_tm: bool, user_pk: User.pk = None):
    """
    overlay_pk : id from Overlay model object
    target: abbreviation of language to translate to
    user: User.
    """
    overlay = Overlay.objects.get(pk=overlay_pk)

    source = overlay.source_lang
    logger.info("Translating page: %s", overlay)
    logger.info("Source language: %s", source)
    logger.info("Target language: %s", target)
    logger.info("Using TM: %s", use_tm)

    if source == target:
        raise ValueError(f'Target language should be different from the source language. Source = {source}')

    activity_log = ActivityLog.objects.create(
        overlay=overlay,
        page=overlay.page,
        type=ActivityLogType.TRANSLATION,
        state=ActivityLogState.PROCESSING
    )

    if user_pk:
        activity_log.user = User.objects.get(pk=user_pk)
        activity_log.save()

    logger.info("Created activity log")

    conn = CEFeTranslationConnector()

    # Blocking translation request
    try:
        with overlay.get_file().open("rb") as f:
            xml_trans = conn.translate_xml(f, source, target, use_tm)

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
