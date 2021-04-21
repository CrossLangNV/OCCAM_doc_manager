from django.urls import path
from rest_framework import routers
from .views import DocumentViewSet, OverlayViewSet, PageListAPIView

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
# router.register('api/pages', PageViewSet, 'pages')
router.register('api/overlays', OverlayViewSet, 'overlays')

urlpatterns = router.urls

urlpatterns.extend(
    [
        path('api/pages', PageListAPIView.as_view(), name='pages_list_api')
    ]
)