import base64
import io
import json
import logging
import os
import zipfile
from datetime import date
from io import BytesIO

import xmltodict as xmltodict
from django.forms import model_to_dict
from django.http.response import HttpResponse
from minio import Minio, ResponseError
from minio.error import BucketAlreadyOwnedByYou, BucketAlreadyExists
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document, Page, Overlay, Label, LayoutAnalysisModel, Website, Metadata, Geojson
from documents.processing.file_upload import pdf_image_generator
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer, LabelSerializer, \
    LayoutAnalysisModelSerializer, WebsiteSerializer
from documents.tm_connector import MouseTmConnector
from oaipmh.connector import ConnectorDSpaceREST
from oaipmh.models import CommunityAdd, CollectionAdd, ItemAdd
from scheduler.classification_tasks import classify_document_pipeline, classify_scanned
from scheduler.ocr_tasks import ocr_page_pipeline, xml_lang_detect
from scheduler.translation_tasks import translate_overlay

API_KEY_PERO_OCR = os.environ['API_KEY_PERO_OCR']
URL_DSPACE = os.environ['URL_DSPACE']
EMAIL_DSPACE = os.environ['EMAIL_DSPACE']
PASSWORD_DSPACE = os.environ['PASSWORD_DSPACE']
OCCAM_COMMUNITY_NAME = "OCCAM web app"
OCCAM_COLLECTION_NAME = "Documents"

PDF_CONTENT_TYPE = 'application/pdf'
FILE = 'file'
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
        website = self.request.GET.get("website", "")

        if query:
            q = q.filter(name__icontains=query)

        if website:
            q = q.filter(website__name__iexact=website)
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

        file = request.data.get(FILE)

        # PDF, extract pages
        if file and file.content_type == PDF_CONTENT_TYPE:
            pdf_read = file.read()  # file is gone after reading

            # Check if the PDF is a scanned document
            # TODO if detected that the file is not a scanned document,
            #  Show a warning message that there is no need to OCR.
            b_scanned = classify_scanned(pdf_read)

            document_id = request.data[DOCUMENT]
            document = Document.objects.get(pk=document_id)

            page_ids = []

            for i, im in enumerate(pdf_image_generator(pdf_read)):
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

                label = Label.objects.update_or_create(page=page, name='scanned document',
                                                       defaults={'name': "scanned", 'value': b_scanned})
                print("Created label: ", label)

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
        file = request.FILES[FILE]

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


class UpdatePageMetadataAPIView(APIView):
    queryset = Metadata.objects.none()

    def post(self, request, format=None, *args, **kwargs):
        page_id = request.data["page_id"]
        metadata_key = request.data["metadata_key"]
        metadata_value = request.data["metadata_value"]

        try:
            Metadata.objects.update_or_create(page_id=page_id, defaults={metadata_key: metadata_value})
            return Response("OK", status=status.HTTP_200_OK)

        except Page.DoesNotExist as e:
            logger.error(e)
            return Response("Page not found", status=status.HTTP_400_BAD_REQUEST)





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


class ExportMetadataAPIView(APIView):
    # TODO: set auth with a cookie, see https://stackoverflow.com/a/23501687, for now no auth
    permission_classes = []
    queryset = Page.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        page_ids = request.data["page_ids"]

        if page_ids:
            self.queryset = self.queryset.filter(pk__in=list(page_ids))
            serializer = PageSerializer()

            # Create a zip file and add every page in it
            z = zipfile.ZipFile("export.zip", 'w', zipfile.ZIP_DEFLATED)
            for page in self.queryset:
                metadata = Metadata.objects.get(page=page)
                z.writestr(metadata.title + '.xml', serializer.get_metadata_xml(page))

            # Save the zip file
            z.close()

            # Read out the zipfile and encode it with base64, return the string to the response
            with open("export.zip", "rb") as f:
                encoded_str = base64.b64encode(f.read())
                return Response(encoded_str, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PublishDocumentAPIView(APIView):
    queryset = Page.objects.all()

    def get(self, request, format=None, *args, **kwargs):
        document_id = self.request.GET.get(DOCUMENT, "")

        if document_id:
            document = Document.objects.get(id=document_id)
            connector = ConnectorDSpaceREST(URL_DSPACE)
            connector.login(EMAIL_DSPACE, PASSWORD_DSPACE)

            # Get the community from OAI-PMH, or create if it didn't exist yet
            communities = connector.get_communities()
            community = next(filter(lambda c: c.name == OCCAM_COMMUNITY_NAME, communities), None)
            community_uuid = community.uuid
            if not community:
                community_response = connector.add_community(CommunityAdd(name=OCCAM_COMMUNITY_NAME))
                community_dict = xmltodict.parse(community_response.tostring())
                community_uuid = community_dict['UUID']

            # Create a new collection for the document and add to OAI-PMH
            collection_response = connector.add_collection(CollectionAdd(name=document.name), community_uuid)
            collection_dict = xmltodict.parse(collection_response.tostring())

            # Create a new item for every page of the document
            for page in self.queryset.filter(document=document_id):
                metadata = Metadata.objects.filter(page=page.id)[0]
                metadata_dict = metadata.__dict__
                item = ItemAdd(name=metadata.title)
                # add to OAI-PMH
                item_response = connector.add_item(item, collection_dict['collection']['UUID'], metadata_dict)
                item_dict = xmltodict.parse(item_response.tostring())
                # add bitstreams to OAI-PMH for page image and for overlay, translations if available
                connector.add_bitstream(page.file, page.file.name, item_dict["item"]["UUID"])
                overlays = Overlay.objects.filter(page=page.id)
                if overlays:
                    overlay = overlays[0]
                    connector.add_bitstream(overlay.file, overlay.file.name, item_dict["item"]["UUID"])
                    geojsons = Geojson.objects.filter(overlay=overlay.id)
                    for geojson in geojsons:
                        connector.add_bitstream(geojson.file, geojson.file.name, item_dict["item"]["UUID"])

            # Save the uuid in the Django document
            document = Document.objects.get(pk=document_id)
            document.oaipmh_collection_id = collection_dict["collection"]["UUID"]
            document.oaipmh_collection_url = URL_DSPACE + collection_dict["collection"]["link"]
            document.save()

            serializer = DocumentSerializer(document, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Invalid document.", status=status.HTTP_400_BAD_REQUEST)


class WebsiteListAPIView(ListCreateAPIView):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
