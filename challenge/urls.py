from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login_page"),
    path("confirmation/<int:challenge_id>/", confirmation),
]
