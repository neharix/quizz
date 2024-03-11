from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path("answerlist/", AnswerListAPIView.as_view()),
    path("answerdetail/<int:pk>/", AnswerDetailAPIView.as_view()),
    path("challengelist/", ChallengeListAPIView.as_view()),
    path("challengedetail/<int:pk>/", ChallengeDetailAPIView.as_view()),
    path("questionlist/", QuestionListAPIView.as_view()),
    path("questiondetail/<int:pk>/", QuestionDetailAPIView.as_view()),
    path("useranswer_create/", UserAnswerAPIView.as_view()),
]
