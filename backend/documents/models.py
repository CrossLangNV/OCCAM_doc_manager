import uuid

from django.core.files import File
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy


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
    file = models.ImageField(upload_to="pages")
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

    def update_image(self, file):
        """ Save a file to the page.

        Example:
            >> page = Page().objects.create()
            >> with open(filename_image, 'rb') as f:
            >>    page.update_image(f)
        """

        with File(file) as django_file:
            self.file.save(file.name, django_file)
            self.save()

    def __str__(self):
        return str(self.file)


class Overlay(models.Model):
    """
    Can be both transcription, translation.
    Saved as Page XML.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(null=True,
                            blank=True,
                            upload_to='overlays')
    translation_file = models.FileField(null=True, blank=True,
                                        upload_to='overlays/trans')
    geojson = models.FileField(null=True,
                               blank=True,
                               upload_to='overlays/geojson')

    page = models.ForeignKey(
        Page,
        related_name="page_overlay",
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO
    # source_lang = # TODO Single language? Use choice and a abbreviation to full name conversion
    # target_lang = # TODO List (again based on choice/list)

    def update_xml(self, file):
        """ Save a file to overlay.

        Example:
            >> overlay = Overlay().objects.create()
            >> with open(filename_xml, 'rb') as f:
            >>    overlay.update_xml(f)

        """
        with File(file) as django_file:
            self.file.save(file.name, django_file)
            self.save()

    def get_file(self):
        return self.file

    def get_translation_file(self):
        return self.translation_file

    def __str__(self):
        return f"Overlay of '{self.page.file.name}'" + ' ' + '*source lang*' + ' ' + '*target lang*'


class LanguageCodes(models.TextChoices):
    NL = 'NL', gettext_lazy('Nederlands')
    EN = 'EN', gettext_lazy('English')
    FR = 'FR', gettext_lazy('Français')
    DE = 'DE', gettext_lazy('Deutsch')


class LangField(models.CharField):
    def __init__(self,
                 *args,
                 choices=LanguageCodes.choices,
                 max_length=2,
                 **kwargs):
        super(LangField, self).__init__(*args,
                                        choices=choices,
                                        max_length=max_length,
                                        **kwargs)


class Geojson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Language of text (can be after translation) (abbreviation)
    lang = LangField()
    overlay = models.ForeignKey(
        Overlay,
        related_name="overlay_geojson",
        on_delete=models.CASCADE,
        unique=False
    )
    # Is this the source overlay?
    original = models.BooleanField()

    # Geojson file
    file = models.FileField(null=True,
                            blank=True,
                            upload_to='overlays/geojson')

    # Language of original document
    source_lang = LangField()
    # Information about the translation engine (if applicable)
    trans_engine = models.CharField(blank=True, max_length=50)

    def update_file(self, file):
        """ Save a geojson file to the geojson object.

        Example:
            >> geojson = Geojson.objects.create(...)
            >> with open(filename_geojson, 'rb') as f:
            >>    geojson.update_file(f)

        """
        with File(file) as django_file:
            self.file.save(file.name, django_file)
            self.save()
