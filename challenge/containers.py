from django.contrib.auth.models import User

from .models import *


class QuestionContainer:
    def __init__(self, question: Question, user: User):
        self.id = question.id
        self.pk = question.pk
        self.content = question.content
        self.complexity = question.complexity
        self.is_answered = (
            True
            if UserAnswer.objects.filter(
                question=question, challenge=question.challenge, user=user
            ).exists()
            else False
        )
