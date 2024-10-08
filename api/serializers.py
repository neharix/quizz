import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from challenge.models import *

from .models import AuthJournal


class UserProfileSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    about = serializers.CharField(max_length=250)

    def create(self, validated_data):
        try:
            user = User.objects.get(id=validated_data["user"])
        except:
            return {"detail": "Ulanyjy tapylmady"}
        profile = Profile.objects.create(user=user, about=validated_data["about"])
        return profile


class UserAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=1000)
    user = serializers.IntegerField()
    question = serializers.IntegerField()

    def create(self, validated_data):
        answer = Answer.objects.get(
            answer=validated_data["answer"],
            question=Question.objects.get(pk=validated_data["question"]),
        )
        question = Question.objects.get(pk=answer.question.pk)
        user = User.objects.get(id=int(validated_data["user"]))
        is_true = True if answer.is_true else False
        return UserAnswer.objects.create(
            question=question, answer=answer, is_true=is_true, user=user
        )


class UserAnswerByIdSerializer(serializers.Serializer):
    answer = serializers.IntegerField()
    user = serializers.IntegerField()

    def create(self, validated_data):
        answer = Answer.objects.get(id=validated_data["answer"])
        question = Question.objects.get(pk=answer.question.pk)
        user = User.objects.get(id=int(validated_data["user"]))
        is_true = True if answer.is_true else False
        return UserAnswer.objects.create(
            question=question, answer=answer, is_true=is_true, user=user
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "answer", "question", "is_image", "image")


class GetResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = (
            "question",
            "challenge",
            "answer",
            "is_true",
            "is_empty",
            "user",
            "answered_at",
        )


class AuthJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthJournal
        fields = ("name", "surname", "username", "password")


class ChallengeSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()
    time_for_event = serializers.IntegerField()
    question_count = serializers.IntegerField()
    is_participated = serializers.BooleanField()


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question", "challenge", "point", "is_image", "image")


class TestSessionSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    challenge = serializers.IntegerField()
    start = serializers.CharField(max_length=100, required=False)
    end = serializers.CharField(max_length=100, required=False)

    def create(self, validated_data):
        challenge = Challenge.objects.get(pk=validated_data["challenge"])
        user = User.objects.get(id=validated_data["user"])
        test_session = TestSession.objects.create(
            challenge=challenge,
            user=user,
            end=datetime.datetime.now()
            + datetime.timedelta(minutes=challenge.time_for_event),
        )
        start = test_session.start.strftime("%Y-%m-%d %H:%M:%S")
        end = test_session.end.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "challenge": challenge.pk,
            "user": user.pk,
            "start": start,
            "end": end,
        }


class UserResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    true_answer = serializers.IntegerField()
    empty_answer = serializers.IntegerField()
    false_answer = serializers.IntegerField()
    percent = serializers.FloatField()
    is_finished = serializers.BooleanField()
