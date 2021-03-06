import io
import json
import os
import uuid
from django.core.files import File
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy

from documents import pagexml2geojson


class LayoutAnalysisModel(models.Model):
    name = models.CharField(default="", max_length=1000)
    description = models.TextField(default="", blank=True)

    # To save the configs of a model.
    config = models.JSONField(blank=True,
                              default=dict
                              )

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return str(self.name)


class LanguageCodes(models.TextChoices):
    NL = "NL", gettext_lazy("Nederlands")
    EN = "EN", gettext_lazy("English")
    FR = "FR", gettext_lazy("Français")
    DE = "DE", gettext_lazy("Deutsch")
    CS = "CS", gettext_lazy("Čeština")


class LangField(models.CharField):
    def __init__(self, *args, choices=LanguageCodes.choices, max_length=2, **kwargs):
        super(LangField, self).__init__(*args, choices=choices, max_length=max_length, **kwargs)


class Website(models.Model):
    name = models.CharField(max_length=200, unique=True)
    content = models.TextField(blank=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default="", max_length=1000)
    content = models.TextField(default="", blank=True)

    class DocumentState(models.TextChoices):
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

    europeana_item_id = models.CharField(max_length=1000, blank=True, null=True)
    oaipmh_collection_id = models.CharField(max_length=1000, blank=True, null=True)
    oaipmh_collection_url = models.URLField(default="", blank=True)

    layout_analysis_model = models.ForeignKey(LayoutAnalysisModel, on_delete=models.SET_NULL, blank=True, null=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, blank=True, null=True)

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ImageField(upload_to="pages")
    deleted = models.BooleanField(default=False)
    image_hash = models.TextField(null=True, blank=True)

    document = models.ForeignKey(
        Document,
        related_name="document_page",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]

    def update_image(self, file):
        """Save a file to the page.

        Example:
            >> page = Page().objects.create()
            >> with open(filename_image, 'rb') as f:
            >>    page.update_image(f)
        """

        with File(file) as django_file:
            name = os.path.split(file.name)[-1]

            self.file.save(name, django_file)
            self.save()

    def __str__(self):
        return str(self.file)


class Overlay(models.Model):
    """
    Can be both transcription, translation.
    Saved as Page XML.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True, blank=True, upload_to="overlays")
    translation_file = models.FileField(null=True, blank=True, upload_to="overlays/trans")

    page = models.ForeignKey(
        Page,
        related_name="page_overlay",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    source_lang = LangField()

    class Meta:
        ordering = ["-created_at"]

    def update_xml(self, file):
        """Save a file to overlay.

        Example:
            >> overlay = Overlay().objects.create()
            >> with open(filename_xml, 'rb') as f:
            >>    # f.name = '<filename>'
            >>    overlay.update_xml(f)

        """
        with File(file) as django_file:
            name = os.path.split(file.name)[-1]

            self.file.save(name, django_file)
            self.save()

        self.create_geojson()

    def update_transl_xml(self, file, target: str):
        """Save a file to the translation overlay.

        Example:
            >> overlay = Overlay().objects.create()
            >> with open(filename_transl_xml, 'rb') as f:
            >>    # f.name = '<filename>'
            >>    overlay.update_xml(f)

        """

        with File(file) as django_file:
            name = os.path.split(file.name)[-1]

            self.translation_file.save(name, django_file)

            self.save()

        self.create_geojson(target=target)

    def create_geojson(self, target: str = None):
        """
        Creates

        source: language code of original document
        target: (Optional) language code of targeted language
        """

        if target is None:

            assert self.file, "Only make sense if overlay xml exists"

            # Create Geojson overlay and save to the object
            with self.file.open() as f:
                geojson = pagexml2geojson.main(f)
                # logger.info(geojson)

        else:
            assert self.translation_file, "Only make sense if overlay xml exists"

            # Create Geojson overlay and save to the object
            with self.translation_file.open() as f:
                geojson = pagexml2geojson.main(f, target=target)
                # logger.info(geojson)

        original = target is None
        if original:  # Original file
            geojson_object, _ = Geojson.objects.update_or_create(
                overlay=self, original=original,
                defaults={'lang': self.source_lang}
            )
        else:
            geojson_object, _ = Geojson.objects.update_or_create(
                overlay=self, original=original, lang=target,
            )

        basename, _ = os.path.splitext(self.file.name)
        with io.BytesIO(json.dumps(geojson).encode("utf-8")) as f:
            f.name = basename + ".geojson"
            geojson_object.update_file(f)

    def get_file(self):
        return self.file

    def get_translation_file(self):
        return self.translation_file

    def __str__(self):
        return f"Overlay of '{self.page.file.name}'" + " " + "*source lang*" + " " + "*target lang*"


class Geojson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Language of text (can be after translation) (abbreviation)

    lang = LangField()
    overlay = models.ForeignKey(Overlay, related_name="overlay_geojson", on_delete=models.CASCADE, unique=False)
    # Is this the source overlay?
    original = models.BooleanField()

    # Geojson file
    file = models.FileField(null=True, blank=True, upload_to="overlays/geojson")

    # Information about the translation engine (if applicable)
    trans_engine = models.CharField(blank=True, max_length=50)

    class Meta:
        ordering = ["-overlay"]

    def update_file(self, file):
        """Save a geojson file to the geojson object.

        Example:
            >> geojson = Geojson.objects.create(...)
            >> with open(filename_geojson, 'rb') as f:
            >>    geojson.update_file(f)

        """
        with File(file) as django_file:
            name = os.path.split(file.name)[-1]

            self.file.save(name, django_file)
            self.save()

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class DocumentTypePrediction(models.Model):
    name = models.CharField(default="", max_length=1000)
    description = models.TextField(default="", null=True, blank=True)
    certainty = models.TextField(default="", null=True, blank=True)
    prediction = models.BooleanField(null=True, blank=True)
    label = models.TextField(default="", blank=True, null=True)

    page = models.ForeignKey(
        Page,
        related_name="page_doc_type_pred",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name)
    
    
class Metadata(models.Model):
    title = models.CharField(default="", max_length=200)
    creator = models.CharField(default="", max_length=200)
    subject = models.CharField(default="", max_length=200)
    description = models.CharField(default="", max_length=200)
    publisher = models.CharField(default="", max_length=200)
    contributor = models.CharField(default="", max_length=200)
    date = models.CharField(default="", max_length=200)
    type = models.CharField(default="", max_length=200)
    format = models.CharField(default="", max_length=200)
    identifier = models.CharField(default="", max_length=200)
    source = models.CharField(default="", max_length=200)
    language = models.CharField(default="", max_length=200)
    relation = models.CharField(default="", max_length=200)
    coverage = models.CharField(default="", max_length=200)
    rights = models.CharField(default="", max_length=200)

    page = models.ForeignKey(
        Page,
        related_name="page_metadata",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Metadata of {str(self.title)}"
