from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Answer, Challenge, Question
from .serializers import (
    AnswerSerializer,
    ChallengeSerializer,
    QuestionSerializer,
    UserAnswerSerializer,
)


class AnswerAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


class ChallengeAPIView(generics.ListAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer


class QuestionAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class UserAnswerAPIView(APIView):
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"output": "Success!"})
