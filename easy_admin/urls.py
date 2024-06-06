from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", main, name="easy_tools"),
    path("challenge_results/", challenge_results, name="challenge_results"),
    path("challenge_results/<int:challenge_id>/", challenge_result),
    path("side/", side),
    path("get_private/<int:challenge_id>/<int:user_id>/", export_user_result_short),
    path("get_detailed/<int:challenge_id>/<int:user_id>/", export_user_result),
]
