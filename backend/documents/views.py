from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions

from documents.models import Document, Image
from documents.serializers import DocumentSerializer, ImageSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = DocumentSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ImageSerializer