import datetime
import random

import pytz
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.models import *

from .custom_containers import ChallengeContainer, UserResult
from .models import *
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
    def get(self, request: HttpRequest):
        date = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        challenges_queryset = Challenge.objects.all().filter(
            date_finish__gte=date, date_start__lte=date, is_public=True
        )
        challenges = []
        for challenge in challenges_queryset:
            is_participated = (
                True
                if len(
                    TestSession.objects.filter(challenge=challenge, user=request.user)
                )
                != 0
                else False
            )
            challenges.append(
                ChallengeContainer(
                    challenge.pk,
                    challenge.name,
                    challenge.time_for_event,
                    challenge.questions_count,
                    is_participated,
                )
            )

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
                    "question_count": challenge.questions_count,
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

    share_of_questions = challenge.questions_count // 3
    rest_of_questions = challenge.questions_count % 3

    easy_temp = [
        question
        for question in Question.objects.filter(
            challenge=challenge, complexity=Complexity.objects.get(level="Ýeňil")
        )
    ]
    random.shuffle(easy_temp)
    medium_temp = [
        question
        for question in Question.objects.filter(
            challenge=challenge, complexity=Complexity.objects.get(level="Ortaça")
        )
    ]
    random.shuffle(medium_temp)
    hard_temp = [
        question
        for question in Question.objects.filter(
            challenge=challenge, complexity=Complexity.objects.get(level="Kyn")
        )
    ]
    random.shuffle(hard_temp)

    easy_questions = easy_temp[:share_of_questions]
    medium_questions = medium_temp[:share_of_questions]
    hard_questions = hard_temp[:share_of_questions]

    questions = easy_questions + medium_questions + hard_questions

    for i in range(rest_of_questions):
        questions.append(
            random.choice(
                Question.objects.exclude(pk__in=[question.pk for question in questions])
            )
        )

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
def timeout_api_view(request: HttpRequest):
    if request.method == "POST":
        challenge = Challenge.objects.get(pk=request.data["challenge"])
        questions = Question.objects.filter(challenge=challenge)
        user_answers = UserAnswer.objects.filter(user=request.user, challenge=challenge)
        unanswered_questions = []
        for question in questions:
            is_answered = False
            for user_answer in user_answers:
                if user_answer.question.pk == question.pk:
                    is_answered = True
                    break
            if is_answered == False:
                unanswered_questions.append(question)
        for unanswered_question in unanswered_questions:
            UserAnswer.objects.create(
                challenge=challenge,
                question=unanswered_question,
                answer=None,
                is_true=False,
                is_empty=True,
                user=request.user,
                answered_at=datetime.datetime.now(),
            )
    return Response({"detail": "Success"})


@permission_classes((IsAdminUser))
@api_view(http_method_names=["GET"])
def get_current_user_data(request: HttpRequest, challenge_pk: int):
    if request.method == "GET":
        challenge = Challenge.objects.get(pk=challenge_pk)
        sessions = TestSession.objects.filter(challenge=challenge)
        users = [session.user for session in sessions]
        questions = Question.objects.filter(challenge=challenge)

        user_results = []
        pk = 0
        for user in users:
            session = TestSession.objects.get(challenge=challenge, user=user)
            now = datetime.datetime.now(datetime.timezone.utc)

            timezone = pytz.timezone("Asia/Ashgabat")
            if session.end > now.astimezone(timezone):
                is_finished = False
            else:
                is_finished = True

            pk += 1
            user_answers = []
            for question in questions:
                try:
                    user_answers.append(
                        UserAnswer.objects.get(user=user, question=question)
                    )
                except:
                    pass
            user_results.append(
                UserResult(
                    pk,
                    challenge.pk,
                    user,
                    user_answers,
                    session,
                    is_finished,
                    challenge.questions_count,
                )
            )
        serializer = UserResultSerializer(user_results, many=True)
        return Response(serializer.data)


@permission_classes((IsAdminUser))
@api_view(http_method_names=["GET"])
def get_current_user_data_for_chart(request: HttpRequest, challenge_pk: int):
    if request.method == "GET":
        challenge = Challenge.objects.get(pk=challenge_pk)
        sessions = TestSession.objects.filter(challenge=challenge)
        users = [session.user for session in sessions]
        questions = Question.objects.filter(challenge=challenge)

        user_results = []
        pk = 0
        for user in users:
            session = TestSession.objects.get(challenge=challenge, user=user)
            now = datetime.datetime.now(datetime.timezone.utc)

            timezone = pytz.timezone("Asia/Ashgabat")
            if session.end > now.astimezone(timezone):
                is_finished = False
            else:
                is_finished = True

            pk += 1
            user_answers = []
            for question in questions:
                try:
                    user_answers.append(
                        UserAnswer.objects.get(user=user, question=question)
                    )
                except:
                    pass
            user_results.append(
                UserResult(
                    pk,
                    challenge.pk,
                    user,
                    user_answers,
                    session,
                    is_finished,
                    challenge.questions_count,
                )
            )
            user_results.sort(key=lambda e: e.true_answer)
            user_results.reverse()
        serializer = UserResultSerializer(user_results, many=True)
        return Response(serializer.data)


@permission_classes((IsAdminUser,))
@api_view(http_method_names=["GET"])
def equalize_question_complexity_amount(request: HttpRequest, challenge_pk: int):
    challenge = Challenge.objects.get(pk=challenge_pk)

    questions = Question.objects.filter(challenge=challenge)

    share_of_questions = len(questions) // 3
    rest_of_questions = len(questions) % 3

    complexities = Complexity.objects.all()
    complexity_index = 0
    counter = 0
    for question in questions:
        try:
            if counter < share_of_questions:
                question.complexity = complexities[complexity_index]
            question.save()
            counter += 1
            if counter == share_of_questions:
                complexity_index += 1
                counter = 0

        except IndexError:
            question.complexity = random.choice(complexities)
            question.save()
    return Response({"detail": "Success"})


@permission_classes((IsAuthenticated,))
@api_view(http_method_names=["POST"])
def confirmation_api_view(request: HttpRequest):
    if request.FILES.get("photo"):
        ConfirmationImage.objects.create(
            image=request.FILES["photo"], user=request.user
        )
        return Response({"detail": "Success"})
    return Response({"detail": "File not found"})
