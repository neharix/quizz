import pytz
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


class UserResult:
    def __init__(
        self,
        number: int,
        challenge_id: int,
        user: User,
        user_answers: list,
        session: TestSession,
        is_finished: bool,
        questions_count: int,
    ) -> None:
        self.id = number
        self.user_id = user.pk
        self.challenge_id = challenge_id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.start = session.start.astimezone(pytz.timezone("Asia/Ashgabat"))
        self.end = session.end.astimezone(pytz.timezone("Asia/Ashgabat"))
        self.is_finished = is_finished
        if len(user_answers) != 0:
            self.true_answer = sum(
                [1 if answer.is_true else 0 for answer in user_answers]
            )
            self.empty_answer = sum(
                [1 if answer.is_empty else 0 for answer in user_answers]
            )
            self.false_answer = (
                sum([0 if answer.is_true else 1 for answer in user_answers])
                - self.empty_answer
            )
            self.percent = round((self.true_answer / questions_count) * 100, 2)
        else:
            self.true_answer = 0
            self.false_answer = 0
            self.empty_answer = 0
            self.percent = 0
