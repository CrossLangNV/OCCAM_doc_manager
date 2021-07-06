import logging
import os

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document, Page, Overlay, Label, LayoutAnalysisModel
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer, LabelSerializer, \
    LayoutAnalysisModelSerializer
from documents.tm_connector import MouseTmConnector
from scheduler.ocr_tasks import ocr_page_pipeline, upload_overlay_pipeline, xml_lang_detect
from scheduler.translation_tasks import translate_overlay

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']

logger = logging.getLogger(__name__)


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

    def get_queryset(self):
        q = Document.objects.filter(user=self.request.user)
        query = self.request.GET.get("query", "")

        if query:
            q = q.filter(name__icontains=query)

        return q.order_by('-updated_at')

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        return self.create(request, *args, **kwargs)


class DocumentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class PageListAPIView(ListCreateAPIView):
    queryset = Page.objects.all()
    pagination_class = BigResultsSetPagination
    serializer_class = PageSerializer

    def get_queryset(self):
        q = Page.objects.all()
        document_id = self.request.GET.get("document", "")

        if document_id:
            q = q.filter(document__id=str(document_id))

        return q


class LabelsListAPIView(ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def get_queryset(self):
        q = Label.objects.all()
        page_id = self.request.GET.get("pageId", "")
        name = self.request.GET.get("labelName", "")

        if page_id:
            q = q.filter(page__id=str(page_id))

        if name:
            q = q.filter(name=name)

        return q


class OverlayListAPIView(ListCreateAPIView):
    queryset = Overlay.objects.all()
    pagination_class = BigResultsSetPagination
    serializer_class = OverlaySerializer

    def get_queryset(self):
        q = Overlay.objects.all()
        page_id = self.request.GET.get("page", "")

        if page_id:
            q = q.filter(page__id=str(page_id))

        return q

    def post(self, request, *args, **kwargs):
        page_id = request.POST["page"]
        file = request.FILES["file"]

        page = Page.objects.get(pk=page_id)
        source_lang = xml_lang_detect(file)  # TODO check if this works...
        overlay, _ = Overlay.objects.update_or_create(page=page,
                                                      defaults={'file': file,
                                                                'source_lang': source_lang}
                                                      )

        overlay.create_geojson()

        upload_overlay_pipeline.delay(page_id)
        return Response("Uploaded.", status=status.HTTP_201_CREATED)


class LayoutAnalysisModelsAPIView(ListCreateAPIView):
    queryset = LayoutAnalysisModel.objects.all()
    serializer_class = LayoutAnalysisModelSerializer


class OverlayDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer


class PageDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class TranslatePageAPIView(APIView):
    queryset = Page.objects.none()

    def post(self, request, format=None, *args, **kwargs):
        overlay = request.data["overlay"]
        target = request.data["target"]
        user = request.data["user"]

        logger.info("Starting celery task for translation")

        translate_overlay.delay(overlay, target, user=user)

        return Response("Translation task launched", status=status.HTTP_201_CREATED)


class PageLaunchOCRAPIView(APIView):
    queryset = Page.objects.none()

    def post(self, request, format=None, *args, **kwargs):
        page_id = request.data["page"]
        user = request.data["user"]
        engine_pk = request.data["engine_pk"]

        ocr_page_pipeline.delay(page_id, str(engine_pk), user=user)

        logger.info("Starting celery task for translation")

        return Response("OCR Task launched", status=status.HTTP_201_CREATED)


class TmxUploadAPIView(APIView):
    queryset = Page.objects.none()

    def post(self, request, format=None, *args, **kwargs):
        tmx = request.FILES.get('tmx')
        conn = MouseTmConnector()
        conn.import_tmx("", "", tmx)

        return Response("Uploaded TMX file", status=status.HTTP_201_CREATED)


class TmStatsAPIView(APIView):
    queryset = Page.objects.none()

    def get(self, request, format=None, *args, **kwargs):
        conn = MouseTmConnector()
        langpairs = conn.get_available_langpairs("")
        results = {}

        for langpair in langpairs:
            amount_tus = conn.get_tu_amount("", langpair)
            results[langpair] = amount_tus

        return Response(results)
