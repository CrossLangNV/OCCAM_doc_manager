from django.contrib import admin

# Register your models here.
from documents.models import Document, Page, Overlay, Geojson, Label, LayoutAnalysisModel, Website, Metadata


class DocumentAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at", "user")


class PageAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")


class OverlayAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")


class GeojsonAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")


class LabelAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at", "name")


class MetadataAdmin(admin.ModelAdmin):
    list_filter = ("created_at", "updated_at")


admin.site.register(Document, DocumentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Overlay, OverlayAdmin)
admin.site.register(Geojson, GeojsonAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(LayoutAnalysisModel)
admin.site.register(Website)
admin.site.register(Metadata, MetadataAdmin)
