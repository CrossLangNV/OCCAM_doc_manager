from django.db import models
from django.utils import timezone

from documents.models import Page


class RequestState(models.TextChoices):
    CREATED = "Created"
    WAITING = "Waiting"
    STARTED = "Started"
    IN_PROGRESS = "In Progress"
    FAILED = "Failed"
    SUCCESS = "Success"


class OcrRequest(models.Model):
    page = models.ForeignKey(
        Page,
        related_name="ocr_request_page",
        on_delete=models.CASCADE,
    )

    endpoint = models.TextField(null=True, blank=True)

    state = models.CharField(
        max_length=50,
        choices=RequestState.choices,
        default=RequestState.CREATED,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]


class TranslationRequest(models.Model):
    page = models.ForeignKey(
        Page,
        related_name="translation_request_page",
        on_delete=models.CASCADE,
    )

    endpoint = models.TextField(null=True, blank=True)

    state = models.CharField(
        max_length=50,
        choices=RequestState.choices,
        default=RequestState.CREATED,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
