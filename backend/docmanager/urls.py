from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from docmanager import settings

urlpatterns = [
    path("", RedirectView.as_view(url="admin/", permanent=True)),

    path('social-auth/', include('social_django.urls', namespace='social-view')),
    path('auth/', include('rest_framework_social_oauth2.urls')),

    path('admin/', admin.site.urls),
    path('documents/', include(('documents.urls', 'documents'), namespace='documents')),
    path('activitylogs/', include(('activitylogs.urls', 'activitylogs'), namespace='activitylogs')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)