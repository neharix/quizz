from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import echo

urlpatterns = [
    path("superuser/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("admin/", include("easy_admin.urls")),
    path("echo/", echo),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
