import io
import logging
import os

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document, Page, Overlay, Label, LayoutAnalysisModel
from documents.processing.file_upload import pdf_image_generator
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer, LabelSerializer, \
    LayoutAnalysisModelSerializer
from documents.tm_connector import MouseTmConnector
from scheduler.classification_tasks import classify_document_pipeline
from scheduler.ocr_tasks import ocr_page_pipeline, xml_lang_detect
from scheduler.translation_tasks import translate_overlay

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']

PDF_CONTENT_TYPE = 'application/pdf'
DOCUMENT = "document"
KEY_PAGE_ID = "PageId"
KEY_LABEL_NAME = 'labelName'

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
        q = Document.objects.all()
        query = self.request.GET.get("query", "")
        show_demo_content = self.request.GET.get("showDemoContent", "")

        if query:
            q = q.filter(name__icontains=query)

        if show_demo_content == "true":
            print("show_demo_content = true")
            q = q.filter(user=None)
        else:
            q = q.filter(user=self.request.user)

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
        document_id = self.request.GET.get(DOCUMENT, "")

        if document_id:
            q = q.filter(document__id=str(document_id))

        return q

    def post(self, request, *args, **kwargs):
        """
        If a PDF is uploaded, it will be converted to individual pages/images.

        Args:
            request:
            *args:
            **kwargs:

        Returns:

        """

        # PDF, extract pages

        FILE = 'file'

        file = request.data.get(FILE)

        if file and file.content_type == PDF_CONTENT_TYPE:

            document_id = request.data[DOCUMENT]
            document = Document.objects.get(pk=document_id)

            page_ids = []

            for i, im in enumerate(pdf_image_generator(file.read())):
                data_i = request.data.copy()
                data_i[FILE] = im  # outputIO

                outputIO = io.BytesIO()
                im.save(outputIO, format=im.format,
                        quality=100)

                # needs a name in order to save it
                outputIO.name = os.path.splitext(os.path.split(file.name)[-1])[0] + f'_{i}.jpg'

                page = self.queryset.create(document=document)
                page.update_image(outputIO)

                page_id = page.id
                classify_document_pipeline.delay(page_id)

                page_ids.append(page_id)

            page_queryset = self.queryset.filter(id__in=page_ids)
            serializer = self.get_serializer(page_queryset, many=True)

        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            classify_document_pipeline.delay(serializer.data.get('id'))

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LabelsListAPIView(ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def get_queryset(self):
        q = Label.objects.all()

        page_id = self.request.GET.get(KEY_PAGE_ID, "")
        name = self.request.GET.get(KEY_LABEL_NAME, "")

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
        source_lang = xml_lang_detect(file)
        overlay, _ = Overlay.objects.update_or_create(page=page,
                                                      defaults={'file': file,
                                                                'source_lang': source_lang}
                                                      )

        overlay.create_geojson()

        serializer = self.get_serializer(overlay)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        use_tm = request.data["useTM"]
        user_pk = request.user.pk

        logger.info("Starting celery task for translation")

        translate_overlay.delay(overlay, target, use_tm, user_pk=user_pk)

        return Response("Translation task launched", status=status.HTTP_201_CREATED)


class PageLaunchOCRAPIView(APIView):
    queryset = Page.objects.none()

    def post(self, request, format=None, *args, **kwargs):
        page_pk = request.data["page"]
        engine_pk = request.data["engine_pk"]
        user_pk = request.user.pk

        ocr_page_pipeline.delay(page_pk, str(engine_pk), user_pk=user_pk)

        logger.info("Starting celery task for OCR")

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
        results = []

        for langpair in langpairs:
            amount_tus = conn.get_tu_amount("", langpair)
            results.append({
                'langpair': langpair,
                'amount': amount_tus
            })

        return Response(results)
