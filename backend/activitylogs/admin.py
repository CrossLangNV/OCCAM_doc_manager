from django.contrib import admin

from activitylogs.models import OcrRequest, TranslationRequest

admin.site.register(OcrRequest)
admin.site.register(TranslationRequest)
