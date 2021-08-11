import uuid

from django.db import models


class BranchUnit(models.Model):
    name = models.TextField(default="", blank=True)


class Function(models.Model):
    name = models.CharField(default="", max_length=1000)
    job_holder = models.CharField(default="", max_length=1000)
    date = models.CharField(default="", max_length=100)


class ProfessionalCompetence(models.Model):
    name = models.CharField(default="", max_length=1000)


class Attribute(models.Model):
    name = models.TextField(default="", blank=True)


class Permit(models.Model):
    name = models.TextField(default="", blank=True)


class BtwNacebelActivity(models.Model):
    name = models.TextField(default="", blank=True)


class RszNacebelActivity(models.Model):
    name = models.TextField(default="", blank=True)


class LinkedEntity(models.Model):
    name = models.TextField(default="", blank=True)


class ExternalLink(models.Model):
    name = models.CharField(default="", max_length=1000)
    url = models.URLField(default="")


# Create your models here.
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # General
    company_number = models.CharField(default="", max_length=100)
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

    branch_units = models.ManyToManyField(BranchUnit, related_name="company_branch_units")

    # Functions
    functions = models.ManyToManyField(Function, related_name="company_functions")

    # Professional Competencies
    professional_competencies = models.ManyToManyField(ProfessionalCompetence,
                                                       related_name="company_professional_competencies")

    # Attributes
    attributes = models.ManyToManyField(Attribute, related_name="company_attributes")

    # Permits
    permits = models.ManyToManyField(Permit, related_name="company_permits")

    # BTW-activiteiten Nacebelcode versie 2008(1)
    btw_nacebel_activities = models.ManyToManyField(BtwNacebelActivity, related_name="company_btw_nacebel_activities")

    # RSZ-activiteiten Nacebelcode versie 2008(1)
    rsz_nacebel_activities = models.ManyToManyField(RszNacebelActivity, related_name="company_rsz_nacebel_activities")

    # Financial information
    capital = models.CharField(default="", max_length=1000, blank=True)
    annual_meeting = models.CharField(default="", max_length=1000, blank=True)
    fiscal_year_end_date = models.CharField(default="", max_length=1000, blank=True)
    start_date_exceptional_financial_year = models.CharField(default="", max_length=1000, blank=True)
    end_date_exceptional_financial_year = models.CharField(default="", max_length=1000, blank=True)

    # Links between entities
    links_between_entities = models.ManyToManyField(LinkedEntity, related_name="company_links_between_entities")

    # External links
    external_links = models.ManyToManyField(ExternalLink, related_name="company_external_links")
