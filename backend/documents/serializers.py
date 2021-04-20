from rest_framework import serializers
from documents.models import Document, Page, Overlay


class PageSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Page
        fields = "__all__"


class OverlaySerializer(serializers.ModelSerializer):
    Document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = Overlay
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    document_page = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Document
        fields = "__all__"
