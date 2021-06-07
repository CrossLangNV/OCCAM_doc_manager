from rest_framework import serializers

from activitylogs.models import ActivityLog, ActivityLogType
from activitylogs.serializers import ActivityLogSerializer
from documents.models import Document, Page, Overlay, Geojson, Label


class GeojsonSerializer(serializers.ModelSerializer):
    overlay = serializers.PrimaryKeyRelatedField(queryset=Overlay.objects.all())

    class Meta:
        model = Geojson
        fields = "__all__"


class OverlaySerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    overlay_geojson = GeojsonSerializer(many=True, read_only=True)

    latest_state = serializers.SerializerMethodField()

    def get_latest_state(self, overlay):
        q = ActivityLog.objects.filter(overlay=overlay)
        serializer = ActivityLogSerializer(instance=q, many=True, read_only=True)
        return serializer.data

    class Meta:
        model = Overlay
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())
    page_overlay = OverlaySerializer(many=True, read_only=True)

    image_height = serializers.SerializerMethodField()
    image_width = serializers.SerializerMethodField()
    file = serializers.ImageField()

    latest_ocr_state = serializers.SerializerMethodField()
    latest_translation_state = serializers.SerializerMethodField()

    def get_latest_ocr_state(self, page):
        latest_activity_for_page = ActivityLog.objects.filter(page=page, type=ActivityLogType.OCR)
        if latest_activity_for_page:
            latest_activity_for_page = latest_activity_for_page.latest('created_at')
            serializer = ActivityLogSerializer(instance=latest_activity_for_page, many=False, read_only=True)
            return serializer.data
        else:
            return ""

    def get_latest_translation_state(self, page):
        latest_overlay = Overlay.objects.filter(page=page)
        if latest_overlay:
            latest_overlay = latest_overlay.latest('created_at')

            q = ActivityLog.objects.filter(overlay=latest_overlay, type=ActivityLogType.TRANSLATION)
            serializer = ActivityLogSerializer(instance=q, many=True, read_only=True)
            return serializer.data

    def get_image_height(self, page):
        return page.file.height

    def get_image_width(self, page):
        return page.file.width

    class Meta:
        model = Page
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    document_page = PageSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = "__all__"
