from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import echo
from challenge.views import *
from easy_admin.views import profile_redirect

urlpatterns = [
    path("superuser/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("admin/", include("easy_admin.urls")),
    path("echo/", echo),
    path("", include("challenge.urls")),
    path("logout/", logout_view, name="logout"),
    path("accounts/profile/", profile_redirect, name="profile"),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
