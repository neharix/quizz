import datetime

from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models import Answer, Challenge, Question, TestSession, UserAnswer

from .custom_containers import ChallengeContainer
from .models import AuthJournal
from .serializers import *


def echo(request):
    return HttpResponse(status=200)


class UserProfileAPIView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"output": "Success!"})


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


class ChallengeListAPIView(APIView):
    def get(self, request):
        date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        challenges_queryset = Challenge.objects.all().filter(
            date_finish__gte=date, date_start__lte=date, is_public=True
        )
        challenges = [
            ChallengeContainer(
                challenge.pk,
                challenge.name,
                challenge.time_for_event,
                len(Question.objects.filter(challenge=challenge.pk)),
            )
            for challenge in challenges_queryset
        ]

        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)


class ChallengeAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["pk"]
        try:
            challenge = Challenge.objects.get(pk=key)
            return Response(
                {
                    "pk": challenge.pk,
                    "name": challenge.name,
                    "time_for_event": challenge.time_for_event,
                    "question_count": len(
                        Question.objects.filter(challenge=challenge.pk)
                    ),
                }
            )
        except:
            return Response({"detail": "Не найден объект с таким идентификатором"})

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


class GetChallengeResultAPIView(APIView):
    def get(self, request, **kwargs):
        key = kwargs["pk"]
        challenge = Challenge.objects.get(pk=key)
        user_answers = UserAnswer.objects.filter(user=request.user, challenge=challenge)

        queryset = user_answers
        serializer = GetResultSerializer(queryset, many=True)
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class TestSessionAPIView(APIView):
    def post(self, request: HttpRequest):
        serializer = TestSessionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    permission_classes = (IsAuthenticated,)


class TestSessionUpdateAPIView(APIView):
    def post(self, request: HttpRequest):
        challenge = Challenge.objects.get(pk=request.data["challenge"])
        user = User.objects.get(pk=request.data["user"])
        test_session = TestSession.objects.get(challenge=challenge, user=user)
        test_session.end = datetime.datetime.strptime(
            request.data["date"], "%Y-%m-%d %H:%M:%S"
        )
        test_session.save()
        return Response({"output": "Success!"})

    permission_classes = (IsAuthenticated,)


@permission_classes((IsAuthenticated,))
@api_view(http_method_names=["POST"])
def user_answer_api_view(request: HttpRequest):
    if request.method == "POST":
        if request.data.get("answer"):
            answer = Answer.objects.get(pk=request.data["answer"])
            is_empty = False
        else:
            answer = None
            is_empty = True
        challenge = Challenge.objects.get(pk=request.data["challenge"])
        question = Question.objects.get(pk=request.data["question"])
        user = User.objects.get(id=request.user.id)
        date = datetime.datetime.strptime(request.data["datetime"], "%Y-%m-%d %H:%M:%S")
        if is_empty:
            is_true = False
        else:
            is_true = True if answer.is_true else False
        UserAnswer.objects.create(
            challenge=challenge,
            question=question,
            answer=answer,
            is_true=is_true,
            is_empty=is_empty,
            user=user,
            answered_at=date,
        )
        return Response({"detail": "Success"})
    else:
        return Response({"detail": "Fail"})


@permission_classes((IsAuthenticated,))
@api_view()
def challenge_data_api_view(request: HttpRequest, challenge_pk):
    challenge = Challenge.objects.get(pk=challenge_pk)
    questions = Question.objects.filter(challenge=challenge)
    questions_data = []
    for question in questions:
        try:
            image_path = question.image.url
        except:
            image_path = ""
        question_data = {
            "pk": question.pk,
            "question": question.question,
            "is_image": question.is_image,
            "image": image_path,
        }
        answers = Answer.objects.filter(question=question)
        answers_data = []
        for answer in answers:
            try:
                image_path = answer.image.url
            except:
                image_path = ""

            answers_data.append(
                {
                    "pk": answer.pk,
                    "answer": answer.answer,
                    "question": answer.question.pk,
                    "image": image_path,
                    "is_image": answer.is_image,
                }
            )
        question_data["answers"] = answers_data
        questions_data.append(question_data)
    return Response(questions_data)


@permission_classes((IsAuthenticated,))
@api_view(http_method_names=["POST"])
# FIXME
def timeout_api_view(request: HttpRequest, challenge_pk):
    if request.method == "POST":
        challenge = Challenge.objects.get(pk=request.data["challenge"])
        questions = Question.objects.filter(challenge=challenge)
        user_answers = UserAnswer.objects.filter(user=request.user, challenge=challenge)
    return Response({})
