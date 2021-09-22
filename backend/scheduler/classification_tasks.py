import os

import requests

from activitylogs.models import ActivityLog, ActivityLogState
from celery import shared_task

from documents.metadata_django import MetadataDjango
from documents.models import Page, Metadata, DocumentTypePrediction
from scheduler.tasks import logger, get_activity_log

DOCUMENT_CLASSIFIER_URL = os.environ["DOCUMENT_CLASSIFIER_URL"]
DOC_CLASSIFIER_MODEL_ID = "1"
DOCUMENT_SCANNED_URL = os.environ["DOCUMENT_SCANNED_URL"]


@shared_task
def classify_document_pipeline(page_pk, user_pk=None, activity_log: ActivityLog = None, verbose: int = 1):
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
        activity_log = get_activity_log(page, user_pk=user_pk)

    classify_document(page)
    activity_log.state = ActivityLogState.CLASSIFIED
    activity_log.save()

    if verbose:
        logger.info("Classified page")


def classify_scanned(file, verbose=1) -> dict:
    files = {"file": file}

    r = requests.post(DOCUMENT_SCANNED_URL, files=files)

    res = r.json()

    if verbose:
        print("Classification result: ", res)

    # b_scanned = res.get("prediction")

    return res


def get_document_classification(page, model_id):
    headers = {
        "model-id": DOC_CLASSIFIER_MODEL_ID,
    }

    f = page.file  # image
    files = {"file": f}

    r = requests.post(DOCUMENT_CLASSIFIER_URL, headers=headers, files=files)

    res = r.json()

    print("Classification result: ", res)

    return res


def classify_document(page):
    # Create Metadata object
    generated_metadata = MetadataDjango.from_page(page)
    data = generated_metadata.get_dict()
    print("data: ", data)

    title = ", ".join(data["titles"])
    creators = ", ".join(data["creators"])
    subjects = ", ".join(data["subjects"])
    descriptions = ", ".join(data["descriptions"])
    publishers = ", ".join(data["publishers"])
    contributors = ", ".join(data["contributors"])
    dates = ", ".join(data["dates"])
    types = ", ".join(data["types"])
    formats = ", ".join(data["formats"])
    sources = ", ".join(data["sources"])

    metadata = Metadata.objects.update_or_create(
        page=page,
        title=title,
        creator=creators,
        subject=subjects,
        description=descriptions,
        publisher=publishers,
        contributor=contributors,
        date=dates,
        type=types,
        format=formats,
        source=sources,
    )

    print("Metadata has been saved in Django: ", metadata)

    # POST to Document Classifier

    for i in [1, 2]:
        document_classification_results = get_document_classification(page, i)

        if document_classification_results:
            print("classification results: ", document_classification_results.items())

            name = document_classification_results["name"]
            description = document_classification_results["description"]
            certainty = document_classification_results["certainty"]
            prediction = document_classification_results["prediction"]
            label = document_classification_results["label"]

            pred_obj = DocumentTypePrediction.objects.update_or_create(
                page=page,
                name=name,
                defaults={
                    "description": description,
                    "certainty": certainty,
                    "prediction": prediction,
                    "label": label
                }
            )

            print("Created DocumentTypePrediction object: ", pred_obj)
