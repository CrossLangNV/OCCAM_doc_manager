from rest_framework import routers
from .views import DocumentViewSet, ImageViewSet

router = routers.DefaultRouter()
router.register('api/documents', DocumentViewSet, 'documents')
router.register('api/images', ImageViewSet, 'images')

urlpatterns = router.urls