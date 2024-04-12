from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [path("", tools, name="easy_tools")]
