from django.urls import path

from .views import OverlayTranslationView, PageListAPIView, PageDetailAPIView, TranslatePageAPIView, OverlayListAPIView, \
    DocumentListAPIView, \
    DocumentDetailAPIView, OverlayDetailAPIView, PageLaunchOCRAPIView
from .views import PageTranscriptionView

urlpatterns = [
    path("api/documents", DocumentListAPIView.as_view(), name="document_list_api"),
    path("api/document/<uuid:pk>", DocumentDetailAPIView.as_view(), name="document_detail_api"),

    path('api/pages', PageListAPIView.as_view(), name='pages_list_api'),
    path("api/page/<str:pk>", PageDetailAPIView.as_view(), name="page_api_detail"),
    path("api/pages/translate", TranslatePageAPIView.as_view(), name="translate_page_api"),
    path("api/pages/launch_ocr", PageLaunchOCRAPIView.as_view(), name="page_launch_ocr_task"),

    path('api/overlays', OverlayListAPIView.as_view(), name='overlay_list_api'),
    path("api/overlay/<str:pk>", OverlayDetailAPIView.as_view(), name="overlay_api_detail"),
    # Translate a single overlay.
    path(
        'api/overlay/translation',
        OverlayTranslationView.as_view(),
        name='overlay_translation',
    ),
    # OCR a single page.
    path(
        'api/page/transcription/',
        PageTranscriptionView.as_view(),
        name='page_transcription',
    ),
]
