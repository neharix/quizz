from rest_framework import serializers

from challenge.models import Answer, Challenge, Question, UserAnswer

from .models import AuthJournal


class UserAnswerSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=1000)
    answer = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        question = Question.objects.get(question=validated_data["question"])
        answer = Answer.objects.get(answer=validated_data["answer"])
        is_true = True if answer.is_true else False
        return UserAnswer.objects.create(
            question=question.pk, answer=answer.pk, is_true=is_true
        )


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("answer", "question")


class AuthJournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthJournal
        fields = ("name", "surname", "username", "password")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ("id", "name", "is_public", "date_start", "date_finish")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "question", "challenge", "point")
