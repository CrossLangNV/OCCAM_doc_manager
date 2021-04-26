from django.urls import path
from rest_framework import routers
from .views import PageListAPIView, PageDetailAPIView, TranslatePageAPIView, OverlayListAPIView, DocumentListAPIView, \
    DocumentDetailAPIView

router = routers.DefaultRouter()
# router.register('api/documents', DocumentViewSet, 'documents')
# router.register('api/pages', PageViewSet, 'pages')
# router.register('api/overlays', OverlayViewSet, 'overlays')

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("api/documents", DocumentListAPIView.as_view(), name="document_list_api"),
        path("api/document/<uuid:pk>", DocumentDetailAPIView.as_view(), name="document_detail_api"),

        path('api/pages', PageListAPIView.as_view(), name='pages_list_api'),
        path("api/page/<str:pk>", PageDetailAPIView.as_view(), name="page_api_detail"),
        path("api/pages/translate", TranslatePageAPIView.as_view(), name="translate_page_api"),

        path('api/overlays', OverlayListAPIView.as_view(), name='overlay_list_api'),


    ]
)