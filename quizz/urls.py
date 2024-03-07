from django.contrib import admin
from django.urls import path

from .views import AnswerAPIView, ChallengeAPIView, QuestionAPIView, UserAnswerAPIView

urlpatterns = [
    path("answerlist/", AnswerAPIView.as_view()),
    path("challengelist/", ChallengeAPIView.as_view()),
    path("questionlist/", QuestionAPIView.as_view()),
    path("useranswer_create/", UserAnswerAPIView.as_view()),
]
