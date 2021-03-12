from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('documents/', include(('documents.urls', 'documents'), namespace='documents')),
]
