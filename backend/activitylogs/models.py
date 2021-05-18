from django.db import models
from django.utils import timezone

from documents.models import Page


class ActivityLogState(models.TextChoices):
    CREATED = "Created"
    WAITING = "Waiting"
    STARTED = "Started"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    SUCCESS = "Success"


class ActivityLogType(models.TextChoices):
    OCR = "OCR"
    TRANSLATION = "Translation"


class ActivityLog(models.Model):
    page = models.ForeignKey(
        Page,
        related_name="activity_log_page",
        on_delete=models.CASCADE,
    )

    type = models.CharField(
        max_length=50,
        choices=ActivityLogType.choices,
    )

    state = models.CharField(
        max_length=50,
        choices=ActivityLogState.choices,
        default=ActivityLogState.CREATED,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
