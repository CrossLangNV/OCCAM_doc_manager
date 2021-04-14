from django.contrib import admin

# Register your models here.
from documents.models import Document, Image

admin.site.register(Document)
admin.site.register(Image)