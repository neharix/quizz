from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from api.views import echo
from easy_admin.views import index, logout_view, profile_redirect

urlpatterns = [
    path("superuser/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("admin/", include("easy_admin.urls")),
    path("echo/", echo),
    path("", index, name="home"),
    path("logout/", logout_view, name="logout"),
    path("accounts/profile/", profile_redirect, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
