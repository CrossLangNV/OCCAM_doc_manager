from django.urls import path

from .views import PageListAPIView, PageDetailAPIView, TranslatePageAPIView, OverlayListAPIView, \
    DocumentListAPIView, \
    DocumentDetailAPIView, OverlayDetailAPIView, PageLaunchOCRAPIView, LabelsListAPIView, TmxUploadAPIView, \
    TmStatsAPIView, LayoutAnalysisModelsAPIView, ExportMetadataAPIView, WebsiteListAPIView, UpdatePageMetadataAPIView

urlpatterns = [
    path("api/documents", DocumentListAPIView.as_view(), name="document_list_api"),
    path("api/document/<uuid:pk>", DocumentDetailAPIView.as_view(), name="document_detail_api"),

    path('api/pages', PageListAPIView.as_view(), name='pages_list_api'),
    path("api/page/<str:pk>", PageDetailAPIView.as_view(), name="page_api_detail"),
    path("api/pages/translate", TranslatePageAPIView.as_view(), name="translate_page_api"),
    path("api/pages/launch_ocr", PageLaunchOCRAPIView.as_view(), name="page_launch_ocr_task"),
    path("api/pages/update_metadata", UpdatePageMetadataAPIView.as_view(), name="page_update_metadata_api"),

    path('api/overlays', OverlayListAPIView.as_view(), name='overlay_list_api'),
    path("api/overlay/<str:pk>", OverlayDetailAPIView.as_view(), name="overlay_api_detail"),

    path('api/labels', LabelsListAPIView.as_view(), name='labels_list_api'),

    path('api/tmx/upload', TmxUploadAPIView.as_view(), name='tmx_upload_api'),
    path('api/tm/stats', TmStatsAPIView.as_view(), name='tm_stats_api'),
    path('api/layout_analysis_models', LayoutAnalysisModelsAPIView.as_view(), name='layout_analysis_models_list_api'),

    path('api/export/metadata', ExportMetadataAPIView.as_view(), name='export_metadata_api'),

    path('api/websites', WebsiteListAPIView.as_view(),
         name='website_list_api'),

]
