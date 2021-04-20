from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from documents.models import Document, Page
from documents.serializers import DocumentSerializer, PageSerializer


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
