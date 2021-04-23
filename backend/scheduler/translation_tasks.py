import logging

from documents.models import Page
from celery import shared_task


logger = logging.getLogger(__name__)

@shared_task
def translate_page(page_id, source, target):
    page = Page.objects.get(pk=page_id)
    logger.info("Translating page: %s", page)
    logger.info("Source language: %s", source)
    logger.info("Target language: %s", target)