from rest_framework import serializers

from documents.models import Document, Page, Overlay


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


class OverlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Overlay
        fields = "__all__"
