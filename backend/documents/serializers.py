from rest_framework import serializers

from documents.models import Document, Page, Overlay, Geojson


class GeojsonSerializer(serializers.ModelSerializer):
    overlay = serializers.PrimaryKeyRelatedField(queryset=Overlay.objects.all())

    class Meta:
        model = Geojson
        fields = "__all__"


class OverlaySerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    overlay_geojson = GeojsonSerializer(many=True, read_only=True)

    class Meta:
        model = Overlay
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())
    page_overlay = OverlaySerializer(many=True, read_only=True)

    image_height = serializers.SerializerMethodField()
    image_width = serializers.SerializerMethodField()
    file = serializers.ImageField()

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
