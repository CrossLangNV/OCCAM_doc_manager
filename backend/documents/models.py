import uuid

from django.db import models
from django.utils import timezone


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", max_length=1000)
    content = models.TextField(default="", blank=True)

    class DocumentState(models.Choices):
        NEW = "New"
        WAITING_LAYOUT_ANALYSIS = "Waiting on start of layout analysis."
        RUNNING_LAYOUT_ANALYSIS = "Running layout analysis."
        COMPLETED_LAYOUT_ANALYSIS = "Layout analysis completed."
        WAITING_OCR = "Waiting on start of OCR."
        RUNNING_OCR = "Running OCR."
        COMPLETED_OCR = "OCR completed."

    state = models.CharField(
        max_length=50,
        choices=DocumentState.choices,
        default=DocumentState.NEW,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name + " is added."


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField()
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    image_hash = models.TextField(null=True, blank=True)

    document = models.ForeignKey(
        Document,
        related_name="document_page",
        on_delete=models.CASCADE,
    )

    # TODO: Create a link between TextRegions?

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file)


class Overlay(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True, blank=True)
    translation_file = models.FileField(null=True, blank=True)

    page = models.ForeignKey(
        Page,
        related_name="page_overlay",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
