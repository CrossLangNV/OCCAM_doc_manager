from rest_framework import routers
from .views import DocumentViewSet, PageViewSet

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
router.register('api/pages', PageViewSet, 'pages')

urlpatterns = router.urls