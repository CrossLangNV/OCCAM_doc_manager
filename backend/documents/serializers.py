from rest_framework import serializers
from documents.models import Document, Page


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
