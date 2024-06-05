from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", main, name="easy_tools"),
    path("challenge_results/", challenge_results, name="challenge_results"),
    path("challenge_results/<int:challenge_id>/", challenge_result),
    path("side/", side),
    path("get_docx/", export_data_to_docx),
]
