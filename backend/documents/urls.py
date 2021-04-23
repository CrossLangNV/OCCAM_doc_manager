from django.urls import path
from rest_framework import routers

from .views import PageViewSet, OverlayTranslationView, OverlayDetail, OverlayList
from .views import DocumentViewSet, OverlayViewSet, PageListAPIView, PageDetailAPIView

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
# router.register('api/pages', PageViewSet, 'pages')
router.register('api/overlays', OverlayViewSet, 'overlays')

urlpatterns = router.urls

urlpatterns.extend(
    [
        path('api/pages', PageListAPIView.as_view(), name='pages_list_api'),
        path("api/page/<str:pk>", PageDetailAPIView.as_view(), name="page_api_detail"),

        path('overlays/', OverlayList.as_view()),
        path('overlays/<str:id>/', OverlayDetail.as_view()),
        # Translate a single overlay
        path(
            'api/overlay/translation',
            OverlayTranslationView.as_view(),
            name='overlay_tarnslation',
        ),
    ]
)
