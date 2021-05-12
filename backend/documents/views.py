import logging as logger
import os

from rest_framework import permissions, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from scheduler.ocr_tasks import ocr_page
from scheduler.translation_tasks import translate_overlay

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']


class SmallResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "rows"
    offset_query_param = "offset"


class BigResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    limit_query_param = "rows"
    offset_query_param = "offset"


class DocumentListAPIView(ListCreateAPIView):
    queryset = Document.objects.all()
    pagination_class = SmallResultsSetPagination
    serializer_class = DocumentSerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = Document.objects.all()
        query = self.request.GET.get("query", "")

        if query:
            q = q.filter(name__icontains=query)
            print(query)
            print(q)

        return q.order_by('-updated_at')


class DocumentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]


class PageListAPIView(ListCreateAPIView):
    queryset = Page.objects.all()
    pagination_class = BigResultsSetPagination
    serializer_class = PageSerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = Page.objects.all()
        document_id = self.request.GET.get("document", "")

        if document_id:
            q = q.filter(document__id=str(document_id))

        return q


class OverlayListAPIView(ListCreateAPIView):
    queryset = Overlay.objects.all()
    pagination_class = BigResultsSetPagination
    serializer_class = OverlaySerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        q = Overlay.objects.all()
        page_id = self.request.GET.get("page", "")

        if page_id:
            q = q.filter(page__id=str(page_id))

        return q


class OverlayDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]


class PageDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]


class TranslatePageAPIView(APIView):
    queryset = Page.objects.none()
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        overlay = request.data["overlay"]
        source = request.data["source"]
        target = request.data["target"]

        logger.info("Starting celery task for translation")

        translate_overlay.delay(overlay, source, target)

        return Response("Translation task launched", status=status.HTTP_201_CREATED)


class PageLaunchOCRAPIView(APIView):
    queryset = Page.objects.none()
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        page_id = request.data["page"]

        ocr_page.delay(page_id)

        logger.info("Starting celery task for translation")

        return Response("OCR Task launched", status=status.HTTP_201_CREATED)
