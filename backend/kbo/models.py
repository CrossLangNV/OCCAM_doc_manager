import uuid

from django.db import models


# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General
    company_number = models.CharField(default="", max_length=100, unique=True)
    state = models.CharField(default="", max_length=100)
    legal_status = models.TextField(default="", blank=True)
    start_date = models.CharField(default="", max_length=100)
    name = models.TextField(default="")
    address = models.TextField(default="", blank=True)
    phone_number = models.CharField(default="", max_length=100, blank=True)
    fax_number = models.CharField(default="", max_length=100, blank=True)
    email = models.CharField(default="", max_length=100, blank=True)
    website = models.CharField(default="", max_length=1000, blank=True)
    entity_type = models.CharField(default="", max_length=1000, blank=True)
    legal_form = models.CharField(default="", max_length=1000, blank=True)

    # Financial information
    capital = models.CharField(default="", max_length=1000, blank=True)
    annual_meeting = models.CharField(default="", max_length=1000, blank=True)
    fiscal_year_end_date = models.CharField(default="", max_length=1000, blank=True)
    start_date_exceptional_financial_year = models.CharField(default="", max_length=1000, blank=True)
    end_date_exceptional_financial_year = models.CharField(default="", max_length=1000, blank=True)

    class Meta:
        verbose_name_plural = "companies"


class BranchUnit(models.Model):
    name = models.TextField(default="", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="company_branch_units",
        on_delete=models.CASCADE,
    )


class Function(models.Model):
    name = models.CharField(default="", max_length=1000)
    job_holder = models.CharField(default="", max_length=1000)
    date = models.CharField(default="", max_length=100)
    company = models.ForeignKey(
        Company,
        related_name="company_functions",
        on_delete=models.CASCADE,
    )


class ProfessionalCompetence(models.Model):
    name = models.CharField(default="", max_length=1000)
    company = models.ForeignKey(
        Company,
        related_name="company_professional_competencies",
        on_delete=models.CASCADE,
    )


class Attribute(models.Model):
    name = models.TextField(default="", blank=True)

    company = models.ForeignKey(
        Company,
        related_name="company_attributes",
        on_delete=models.CASCADE,
    )


class Permit(models.Model):
    name = models.TextField(default="", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="company_permits",
        on_delete=models.CASCADE,
    )


class BtwNacebelActivity(models.Model):
    name = models.TextField(default="", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="company_btw_nacebel_activities",
        on_delete=models.CASCADE,
    )


class RszNacebelActivity(models.Model):
    name = models.TextField(default="", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="company_rsz_nacebel_activities",
        on_delete=models.CASCADE,
    )


class LinkedEntity(models.Model):
    name = models.TextField(default="", blank=True)
    company = models.ForeignKey(
        Company,
        related_name="company_links_between_entities",
        on_delete=models.CASCADE,
    )


class ExternalLink(models.Model):
    name = models.CharField(default="", max_length=1000)
    url = models.URLField(default="")
    company = models.ForeignKey(
        Company,
        related_name="company_external_links",
        on_delete=models.CASCADE,
    )
