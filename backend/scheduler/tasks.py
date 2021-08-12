import logging

from django.contrib.auth.models import User

from activitylogs.models import ActivityLog, ActivityLogType
from documents.models import Page

logger = logging.getLogger(__name__)


def get_activity_log(page: Page,
                     user_pk: User.pk = None):
    activity_log = ActivityLog.objects.create(page=page,
                                              type=ActivityLogType.OCR)
    if user_pk:
        user_obj = User.objects.get(pk=user_pk)
        activity_log.user = user_obj
        activity_log.save()

    return activity_log
