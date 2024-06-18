from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", main, name="easy_tools"),
    path("challenges/import_from_xlsx/", import_from_xlsx, name="import_from_xlsx"),
    path("challenges/", challenges, name="challenges"),
    path("editable_challenges/", editable_challenges, name="editable_challenges"),
    path("editable_challenges/add/", add_challenge),
    path("editable_challenges/delete/<int:challenge_id>/", delete_challenge),
    path("editable_challenges/edit/<int:challenge_id>/", edit_challenge),
    path(
        "editable_challenges/edit/<int:challenge_id>/edit_question/<int:question_id>/",
        edit_question,
    ),
    path(
        "editable_challenges/edit/<int:challenge_id>/edit_question/<int:question_id>/edit_answer/<int:answer_id>/",
        edit_answer,
    ),
    path(
        "editable_challenges/edit/<int:challenge_id>/edit_question/<int:question_id>/add_answer/",
        add_answer,
    ),
    path(
        "editable_challenges/edit/<int:challenge_id>/edit_question/<int:question_id>/delete_answer/<int:answer_id>/",
        delete_answer,
    ),
    path(
        "editable_challenges/edit/<int:challenge_id>/delete_question/<int:question_id>/",
        delete_question,
    ),
    path(
        "editable_challenges/edit/<int:challenge_id>/add_question/",
        add_question,
    ),
    path("challenges/<int:challenge_id>/", challenge_result),
    path(
        "challenges/<int:challenge_id>/by_date/<int:year>/<int:month>/<int:day>/",
        challenge_result,
    ),
    path("side/", side),
    path("get_private/<int:challenge_id>/<int:user_id>/", export_user_result_short),
    path(
        "get_private/<int:challenge_id>/<int:user_id>/by_date/<int:year>/<int:month>/<int:day>/",
        export_user_result_short,
    ),
    path("get_detailed/<int:challenge_id>/<int:user_id>/", export_user_result),
    path(
        "get_detailed/<int:challenge_id>/<int:user_id>/by_date/<int:year>/<int:month>/<int:day>/",
        export_user_result,
    ),
    path("get_all/<int:challenge_id>/", export_all_results),
    path(
        "get_all/<int:challenge_id>/by_date/<int:year>/<int:month>/<int:day>/",
        export_all_results,
    ),
]
