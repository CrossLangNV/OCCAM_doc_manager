import os

import requests

from activitylogs.models import ActivityLog, ActivityLogState
from celery import shared_task
from documents.models import Page, Label
from scheduler.tasks import logger, get_activity_log

DOCUMENT_CLASSIFIER_URL = os.environ["DOCUMENT_CLASSIFIER_URL"]
DOC_CLASSIFIER_MODEL_ID = "1"


@shared_task
def classify_document_pipeline(page_pk,
                               user_pk=None,
                               activity_log: ActivityLog = None,
                               verbose: int = 1):
    """

    Args:
        page_pk:
        user_pk:
        activity_log:
        verbose: 0, 1 or 2: 0 to log nothing, 1 to show most important logs, 2 to show everything

    Returns:

    """
    if verbose:
        logger.info("Started classifying document type of : %s", page_pk)

    page = Page.objects.get(pk=page_pk)
    if verbose >= 2:
        logger.info("Started upload for page: %s", page)

    if activity_log is None:
        activity_log = get_activity_log(page,
                                        user_pk=user_pk)

    classify_document(page)
    activity_log.state = ActivityLogState.CLASSIFIED
    activity_log.save()

    if verbose:
        logger.info("Classified page")


def get_document_classification(page):
    headers = {
        "model-id": DOC_CLASSIFIER_MODEL_ID,
    }

    f = page.file  # image
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
