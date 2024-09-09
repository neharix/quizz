from django.contrib import admin
from django.urls import include, path, re_path

from .views import *

urlpatterns = [
    path("", echo),
    path("get-current-data/<int:challenge_pk>/", get_current_user_data),
    path(
        "get-current-data-for-chart/<int:challenge_pk>/",
        get_current_user_data_for_chart,
    ),
    path("create_profile/", UserProfileAPIView.as_view()),
    path("answerlist/", AnswerListAPIView.as_view()),
    path("answerfilter/<int:pk>/", AnswerFilterAPIView.as_view()),
    path("challenge/<int:pk>/", ChallengeAPIView.as_view()),
    path("challengelist/", ChallengeListAPIView.as_view()),
    path("challenge-data/<int:challenge_pk>/", challenge_data_api_view),
    path("useranswer-create/", user_answer_api_view),
    path("timeout/", timeout_api_view),
    path("auth-journal/create", AuthJournalAPIView.as_view()),
    path("auth-journal/<str:username>/", AuthJournalFilterAPIView.as_view()),
    path("useranswers/<int:pk>/", GetChallengeResultAPIView.as_view()),
    path("test-session-create/", TestSessionAPIView.as_view()),
    path("test-session-update/", TestSessionUpdateAPIView.as_view()),
    path("session-auth/", include("rest_framework.urls")),
    path("auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
