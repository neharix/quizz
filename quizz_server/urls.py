from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("superuser/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("admin/", include("easy_admin.urls")),
]
