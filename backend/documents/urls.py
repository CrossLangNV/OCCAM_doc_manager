from rest_framework import routers
from .views import DocumentViewSet, PageViewSet, OverlayViewSet

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
router.register('api/pages', PageViewSet, 'pages')
router.register('api/overlays', OverlayViewSet, 'overlays')

urlpatterns = router.urls