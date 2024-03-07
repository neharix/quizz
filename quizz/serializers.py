from rest_framework import serializers

from .models import Answer, Challenge, Question, UserAnswer


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
        fields = ("answer", "question", "is_true")


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ("name", "date_created")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("name", "question", "challenge", "point")
