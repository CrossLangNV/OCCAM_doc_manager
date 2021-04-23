import requests
from rest_framework import generics, status, mixins, viewsets, permissions, views
from rest_framework import viewsets, permissions, views
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination

from documents.models import Document, Page, Overlay
from documents.serializers import DocumentSerializer, PageSerializer, OverlaySerializer
from rest_framework.parsers import FileUploadParser

import logging as logger

from rest_framework.response import Response

URL_TRANSLATE = 'http://192.168.105.41:9050/translate/xml/blocking'


class SmallResultsSetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = "rows"
    offset_query_param = "offset"


class BigResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    limit_query_param = "rows"
    offset_query_param = "offset"


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.order_by('created_at')
    pagination_class = SmallResultsSetPagination

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]
    serializer_class = DocumentSerializer


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


class PageDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]


class OverlayViewSet(viewsets.ModelViewSet):
    queryset = Overlay.objects.all()
    pagination_class = SmallResultsSetPagination

    # TODO: Remove AllowAny
    permission_classes = [permissions.AllowAny]
    serializer_class = OverlaySerializer



class OverlayList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OverlayDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Overlay.objects.all()
    serializer_class = OverlaySerializer

    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)


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
            "id": "8a69bc31-6997-4a3a-bf90-52127726500f",
            "source": "nl",
            "target": "en"
        }
        """

        # headers = {
        #     'source': 'nl', # TODO change
        #   'target': 'en'  # TODO change
        # }
        headers = request.data

        # overlay0 = next(filter(lambda x: x.xml, Overlay.objects.all()))
        try:
            overlay0 = Overlay.objects.get(id=headers['id'])
        except:
            content = {'message': 'Overlay id not found.'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        with overlay0.xml.open('rb') as f:
            files = {'file': f}

            response = requests.post(URL_TRANSLATE,
                                     headers=headers,
                                     files=files
                                     )

        if response.ok:
            # TODO use overlay0.update_xml instead? This works though.
            # TODO also update filename? Probably not necessary.
            with overlay0.xml.open('wb') as f:
                f.write(response.content)

            # TODO add translated language info to overlay0 object.

        django_response = Response(
            # overlay0,
            response.content,
            status=response.status_code,
            content_type=response.headers['Content-Type'],
            headers=response.headers
        )

        return django_response  # TODO
