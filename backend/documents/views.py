from rest_framework import viewsets, permissions, views
from rest_framework.exceptions import ParseError
from rest_framework.pagination import LimitOffsetPagination

from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from rest_framework.parsers import FileUploadParser

import logging as logger


class SmallResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "rows"
    offset_query_param = "offset"


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.order_by('created_at')
    pagination_class = SmallResultsSetPagination

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]
    serializer_class = DocumentSerializer


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    pagination_class = SmallResultsSetPagination

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]
    serializer_class = PageSerializer


class PageUploadView(views.APIView):
    parser_class = (FileUploadParser, )

    def put(self, request, filename):
        if 'file' not in request.data:
            raise ParseError("Empty content")

        f = request.data['file']
        print(f)






class OverlayViewSet(viewsets.ModelViewSet):
    queryset = Overlay.objects.all()
    pagination_class = SmallResultsSetPagination

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]
    serializer_class = OverlaySerializer