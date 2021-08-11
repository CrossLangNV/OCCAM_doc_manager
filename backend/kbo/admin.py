# Register your models here.
from django.contrib import admin

from kbo.models import Company, Permit, Attribute, Function, ExternalLink, LinkedEntity, RszNacebelActivity, \
    BtwNacebelActivity, BranchUnit, ProfessionalCompetence

admin.site.register(Company)
admin.site.register(Permit)
admin.site.register(Attribute)
admin.site.register(Function)
admin.site.register(ExternalLink)
admin.site.register(LinkedEntity)
admin.site.register(RszNacebelActivity)
admin.site.register(BtwNacebelActivity)
admin.site.register(BranchUnit)
admin.site.register(ProfessionalCompetence)
