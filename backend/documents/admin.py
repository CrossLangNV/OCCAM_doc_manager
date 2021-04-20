from django.contrib import admin

# Register your models here.
from documents.models import Document, Page, Overlay

admin.site.register(Document)
admin.site.register(Page)
admin.site.register(Overlay)