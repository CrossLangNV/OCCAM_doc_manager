from django.db import models
from django.utils import timezone

from documents.models import Page, Overlay


class ActivityLogState(models.TextChoices):
    CREATED = "Created"
    CLASSIFIED = "Classified"
    WAITING = "Waiting"
    STARTED = "Started"
    PROCESSING = "Processing"
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
        null=True
    )

    overlay = models.ForeignKey(
        Overlay,
        related_name="activity_log_overlay",
        on_delete=models.CASCADE,
        null=True
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

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
