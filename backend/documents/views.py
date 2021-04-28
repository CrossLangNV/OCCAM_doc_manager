import io
import logging as logger
import os
import time
import warnings

import requests
from rest_framework import permissions, views, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from documents.models import Document, Page, Overlay
from documents.ocr_connector import get_request_id, upload_file, get_result, check_state
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from scheduler.ocr_tasks import ocr_page
from scheduler.translation_tasks import translate_overlay

URL_TRANSLATE = 'http://192.168.105.41:9050/translate/xml/blocking'

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
        page = request.data["page"]
        source = request.data["source"]
        target = request.data["target"]

        logger.info("Starting celery task for translation")

        translate_overlay.delay(page, source, target)


class PageLaunchOCRAPIView(APIView):
    queryset = Page.objects.none()
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None, *args, **kwargs):
        page_id = request.data["page"]

        ocr_page.delay(page_id)

        logger.info("Starting celery task for translation")

        return Response("Task launched", status=status.HTTP_201_CREATED)


# Deprecated, TODO TO be removed
class OverlayTranslationView(views.APIView):
    """
    Test does this give some info?
    """
    # queryset = Overlay.objects.all()

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self, request,
             format=None):
        """
        Select an overlay, source language and target language
        Updates the overlay with the translated document

        Is saved to the overlay file.

        Content example:
        {
            "id": "0795babb-b098-48fd-a6bc-7f113bc64985",
            "source": "nl",
            "target": "en"
        }
        """

        warnings.warn('This is now part of a Celery task.', DeprecationWarning)

        headers = request.data

        try:
            overlay0 = Overlay.objects.get(id=headers['id'])
        except:
            content = {'message': 'Overlay id not found.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        with overlay0.get_file().open('rb') as f:
            files = {'file': f}

            response = requests.post(URL_TRANSLATE,
                                     headers=headers,
                                     files=files
                                     )

        if response.ok:
            # TODO use overlay0.update_xml instead? This works though.
            # TODO also update filename? Probably not necessary.

            with io.BytesIO(response.content) as f:
                f.name = overlay0.file.name  # Reuse name
                overlay0.update_xml(f)

            # with overlay0.file.open('wb') as f:
            #     f.write(response.content)

            # TODO add translated language info to overlay0 object.

        django_response = Response(
            # overlay0,
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type'],
            headers=response.headers
        )

        return django_response  # TODO


# Deprecated, TODO TO be removed
class PageTranscriptionView(views.APIView):
    """
    Does text region detection and OCR.

    Generates an Overlay
    """
    # TODO still don't know what this does
    queryset = Page.objects.all()

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]

    def post(self,
             request,
             format=None):

        warnings.warn('This is now part of a Celery task.', DeprecationWarning)

        headers = request.data

        try:
            page = Page.objects.get(id=headers['id'])
        except:
            content = {'message': 'Page id is not found.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        page_name = page.file.name

        response_engines = requests.get('https://pero-ocr.fit.vutbr.cz/api/get_engines',
                                        headers={'api-key': API_KEY_PERO_OCR})

        if not response_engines.ok:
            content = {'message': 'PERO-OCR engines not found.',
                       'status code': response_engines.status_code,
                       'content': response_engines.content,
                       }
            return Response(content, status=status.HTTP_418_IM_A_TEAPOT)  # TODO proper status code.

        model_czech = response_engines.json()['engines']['czech_old_printed']
        model_layout = next(filter(lambda x: 'layout' in x['name'], model_czech['models']))
        model_ocr = next(filter(lambda x: 'layout' not in x['name'], model_czech['models']))

        try:
            request_id = get_request_id(page_name)
        except Exception as e:
            content = {'message': "PERO-OCR couldn't retrieve request id",
                       'error': e,
                       }
            return Response(content, status=status.HTTP_418_IM_A_TEAPOT)

        with page.file.open() as file:
            try:
                upload_file(file,
                            request_id=request_id,
                            page_name=page_name,
                            )
            except Exception as e:
                content = {'message': "PERO-OCR couldn't upload image",
                           'error': e,
                           }
                return Response(content, status=status.HTTP_418_IM_A_TEAPOT)

        # Check if finished!
        while True:
            b = check_state(request_id,
                            page_name)

            if b:
                break
            else:  # 'PROCESSED'
                time.sleep(1)

        try:
            overlay_xml = get_result(request_id,
                                     page_name)
        except Exception as e:
            content = {'message': "PERO-OCR couldn't download result",
                       'error': e,
                       }
            return Response(content, status=status.HTTP_418_IM_A_TEAPOT)

        overlay = Overlay().objects.create(page=page)

        with io.BytesIO(overlay_xml) as f:
            overlay.update_xml(f)

        content = {'message': "Successful",
                   }
        return Response(content, status=status.HTTP_200_OK)
