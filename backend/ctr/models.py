import uuid

from django.db import models


# Create your models here.

class CtrCompany(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General
    identification_number = models.CharField(default="", max_length=100, unique=True)
    date_of_creation_and_registration = models.CharField(default="", max_length=100)
    file_number = models.CharField(default="", max_length=100)
    trading_company = models.CharField(default="", max_length=100)
    legal_form = models.CharField(default="", max_length=100)

    class Meta:
        verbose_name_plural = "CTR Companies"


class Residence(models.Model):
    address = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        CtrCompany,
        related_name="ctr_company_residences",
        on_delete=models.CASCADE,
    )
    date = models.CharField(default="", max_length=100)


class ScopeOfBusiness(models.Model):
    name = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        CtrCompany,
        related_name="ctr_company_scope_of_businesses",
        on_delete=models.CASCADE,
    )
    date = models.CharField(default="", max_length=100)

    class Meta:
        verbose_name_plural = "Scope of businesses"


class StatutoryAuthority(models.Model):
    name = models.CharField(default="", max_length=100)
    type = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        CtrCompany,
        related_name="ctr_company_statutory_authorities",
        on_delete=models.CASCADE,
    )
    date = models.CharField(default="", max_length=100)

    class Meta:
        verbose_name_plural = "Statutory Authorities"


class Companion(models.Model):
    companion = models.CharField(default="", max_length=100)
    share = models.CharField(default="", max_length=100)
    lien = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        CtrCompany,
        related_name="ctr_company_companions",
        on_delete=models.CASCADE,
    )
    date = models.CharField(default="", max_length=100)


class OtherFact(models.Model):
    value = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        CtrCompany,
        related_name="ctr_company_other_facts",
        on_delete=models.CASCADE,
    )
    date = models.CharField(default="", max_length=100)
