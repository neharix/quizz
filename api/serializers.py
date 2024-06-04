from django.contrib.auth.models import User
from rest_framework import serializers

from challenge.models import Answer, Challenge, Question, UserAnswer

from .models import AuthJournal


class UserAnswerSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=1000)
    user = serializers.IntegerField()

    def create(self, validated_data):
        answer = Answer.objects.get(answer=validated_data["answer"])
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


class AuthJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthJournal
        fields = ("name", "surname", "username", "password")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = (
            "id",
            "name",
            "is_public",
            "date_start",
            "date_finish",
            "time_for_event",
        )


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question", "challenge", "point", "is_image", "image")
