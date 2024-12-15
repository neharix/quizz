from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_view, name="login_page"),
    path("logout/", logout_view, name="logout_view"),
    path("challenge/<int:challenge_id>/", play_challenge, name="play_challenge"),
    path(
        "challenge/<int:challenge_id>/<int:question_id>/",
        play_challenge,
        name="play_challenge",
    ),
    path("confirmation/<int:challenge_id>/", confirmation),
    path("results/<int:challenge_id>/", results),
    path("timeout/<int:challenge_id>/<int:test_session_id>/", timeout),
    path("change-question/<int:challenge_id>/<int:question_id>/", change_question),
]
