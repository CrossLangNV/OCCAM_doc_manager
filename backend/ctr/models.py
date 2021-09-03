import uuid

from django.db import models


# Create your models here.

class CtrCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General
    identification_number = models.CharField(default="", max_length=100, unique=True)
    business_name = models.TextField(default="", blank=True)
    date_of_creation_and_registration = models.CharField(default="", max_length=100)
    location = models.TextField(default="", blank=True)
    legal_status = models.TextField(default="", blank=True)
    file_reference = models.TextField(default="", blank=True)
    manager = models.TextField(default="", blank=True)
    number_of_members = models.TextField(default="", blank=True)
    representation = models.TextField(default="", blank=True)

    shareholder = models.TextField(default="", blank=True)
    share = models.TextField(default="", blank=True)
    lien = models.TextField(default="", blank=True)
    share_capital = models.TextField(default="", blank=True)


    scope_of_business = models.TextField(default="", blank=True)
    statutory_authorities = models.TextField(default="", blank=True)
    object_of_business = models.TextField(default="", blank=True)
    statutory_body = models.TextField(default="", blank=True)
    shareholders = models.TextField(default="", blank=True)
    other_facts = models.TextField(default="", blank=True)

    class Meta:
        verbose_name_plural = "CTR Companies"

    def __str__(self):
        return str(self.business_name)