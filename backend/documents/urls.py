from django.urls import path
from rest_framework import routers

from .views import DocumentViewSet, ImageViewSet, OverlayViewSet, OverlayTranslationView, OverlayDetail, OverlayList

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
router.register('api/images', ImageViewSet, 'images')
router.register('api/overlays', OverlayViewSet, 'overlays')

urlpatterns = router.urls

urlpatterns.extend(
    [
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
