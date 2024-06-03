from django.http import HttpResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models import Answer, Challenge, Question

from .models import AuthJournal
from .serializers import (
    AnswerSerializer,
    AuthJournalSerializer,
    ChallengeSerializer,
    QuestionSerializer,
    UserAnswerByIdSerializer,
    UserAnswerSerializer,
)


def echo(request):
    return HttpResponse(status=200)


class AnswerListAPIView(generics.ListAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)


class AuthJournalAPIView(generics.CreateAPIView):
    queryset = []
    serializer_class = AuthJournalSerializer
    permission_classes = ()


class AnswerFilterAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["pk"]
        queryset = Answer.objects.filter(question=key)
        serializer = AnswerSerializer(queryset, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class AuthJournalFilterAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["username"]
        queryset = AuthJournal.objects.filter(username=key)
        serializer = AuthJournalSerializer(queryset, many=True)
        return Response(serializer.data)


class ChallengeListAPIView(generics.ListAPIView):
    date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    queryset = Challenge.objects.all().filter(
        date_finish__gte=date, date_start__lte=date, is_public=True
    )
    serializer_class = ChallengeSerializer
    permission_classes = (IsAuthenticated,)


class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)


class ChallengeAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["pk"]
        queryset = Challenge.objects.filter(pk=key)
        if len(queryset) == 0:
            return Response({"detail": "Не найдено данных по заданному ключу"})
        else:
            serializer = ChallengeSerializer(queryset, many=True)
            return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class QuestionFilterAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["pk"]
        queryset = Question.objects.filter(challenge=key)
        if len(queryset) == 0:
            return Response({"detail": "Не найдено данных по заданному ключу"})
        else:
            serializer = QuestionSerializer(queryset, many=True)
            return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class UserAnswerAPIView(APIView):
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"output": "Success!"})

    permission_classes = (IsAuthenticated,)


class UserAnswerByIdAPIView(APIView):
    def post(self, request):
        serializer = UserAnswerByIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"output": "Success!"})

    permission_classes = (IsAuthenticated,)
