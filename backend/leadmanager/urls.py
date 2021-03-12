from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('leads/', include(('leads.urls', 'leads'), namespace='leads')),
]
