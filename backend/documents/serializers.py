from django.forms import model_to_dict
from rest_framework import serializers

from activitylogs.models import ActivityLog, ActivityLogType
from activitylogs.serializers import ActivityLogSerializer
from documents.metadata_django import MetadataDjango
from documents.models import Document, Page, Overlay, Geojson, LayoutAnalysisModel, Website, Metadata, \
    DocumentTypePrediction


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
    metadata = serializers.SerializerMethodField()
    metadata_xml = serializers.SerializerMethodField()

    def get_latest_ocr_state(self, page):
        latest_activity_for_page = ActivityLog.objects.filter(page=page, type=ActivityLogType.OCR)
        if latest_activity_for_page:
            latest_activity_for_page = latest_activity_for_page.latest("created_at")
            serializer = ActivityLogSerializer(instance=latest_activity_for_page, many=False, read_only=True)
            return serializer.data
        else:
            return ""

    def get_latest_translation_state(self, page):
        latest_overlay = Overlay.objects.filter(page=page)
        if latest_overlay:
            latest_overlay = latest_overlay.latest("created_at")

            q = ActivityLog.objects.filter(overlay=latest_overlay, type=ActivityLogType.TRANSLATION)
            serializer = ActivityLogSerializer(instance=q, many=True, read_only=True)
            return serializer.data

    def get_image_height(self, page):
        return page.file.height

    def get_image_width(self, page):
        return page.file.width

    def get_metadata(self, page):
        # metadata = MetadataDjango.from_page(page)
        #
        # data = metadata.get_dict()
        # print("DATA old: ", data)

        metadata = Metadata.objects.filter(page=page)

        if metadata:
            metadata = metadata[0]
            data = model_to_dict(
                metadata,
                fields=[
                    "title",
                    "creator",
                    "subject",
                    "description",
                    "publisher",
                    "contributor",
                    "date",
                    "type",
                    "format",
                    "identifier",
                    "source",
                    "language",
                    "relation",
                    "coverage",
                    "right",
                ],
            )

            page_document_type_pred = page.page_doc_type_pred.all()
            for doc_type_pred in page_document_type_pred:
                # The string representation prediction of BOG vs NBB is in the label instead of prediction (boolean)
                if "scanned" in str(doc_type_pred).lower():
                    data.setdefault(doc_type_pred.name, doc_type_pred.prediction)
                else:
                    data.setdefault(doc_type_pred.name, doc_type_pred.label)

            return data
        else:
            return ""


    def get_metadata_xml(self, page):
        metadata = MetadataDjango.from_page(page)

        return metadata.to_xml()

    class Meta:
        model = Page
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    document_page = PageSerializer(many=True, read_only=True)
    suggested_model = serializers.SerializerMethodField()

    def get_suggested_model(self, document):
        dh_count = 0
        bris_count = 0

        for page in document.document_page.all():
            print("page: ", page)

            page_document_type_pred = page.page_doc_type_pred.all()

            for doc_type_pred in page_document_type_pred:
                if doc_type_pred.name == "Digital Humanities":
                    if doc_type_pred.prediction:
                        dh_count += 1
                    else:
                        bris_count += 1

        return bris_count > dh_count

    class Meta:
        model = Document
        fields = "__all__"


class DocumentTypePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypePrediction
        fields = "__all__"


class LayoutAnalysisModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutAnalysisModel
        fields = "__all__"


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = "__all__"
