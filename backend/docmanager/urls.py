from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from docmanager import settings
from docmanager.views import CurrentUserAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="OCCAM API",
        default_version='v1',
        description="OCCAM (OCR, ClassificAtion & Machine Translation) responds to action line “Integration projects” "
                    "on the integration (and extension) of CEF (Connecting Europe Facility) Automated Translation "
                    "into multilingual digital cross-border services. The Action proposes the integration of image "
                    "classification, Translation Memories (TMs), Optical Character Recognition (OCR), and Machine "
                    "Translation (MT) to support the automated translation of scanned documents – a document type "
                    "that currently cannot be processed by the CEF eTranslation service.",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="occam.info@snippets.local"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("", RedirectView.as_view(url="/admin/", permanent=True)),

    path('social-auth/', include('social_django.urls', namespace='social-view')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('auth/me', CurrentUserAPIView.as_view(), name="current_user_api_view"),

    path('admin/', admin.site.urls),
    path('documents/', include(('documents.urls', 'documents'), namespace='documents')),
    path('activitylogs/', include(('activitylogs.urls', 'activitylogs'), namespace='activitylogs')),
    path('tutorial/', include(('tutorial.urls', 'tutorial'), namespace='tutorial')),
    path('scraper/', include(('scraper.urls', 'scraper'), namespace='scraper')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
