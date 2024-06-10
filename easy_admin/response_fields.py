from django.contrib.auth.models import User

from challenge.models import Challenge, Question, TestSession


class ChallengeResult:
    def __init__(self, number: int, challenge: Challenge):
        self.id = number
        self.name = challenge.name
        self.start = challenge.date_start
        self.end = challenge.date_finish
        self.time_for_event = challenge.time_for_event
        self.pk = challenge.pk

    def __str__(self):
        return self.name


class FQuestion:
    def __init__(self, number: int, question: Question):
        self.id = number
        self.question = question.question
        self.is_image = question.is_image
        self.image = question.image
        self.pk = question.pk

    def __str__(self):
        return self.name


class UserResult:
    def __init__(
        self,
        number: int,
        challenge_id: int,
        user: User,
        user_answers: list,
        session: TestSession,
        is_finished: bool,
    ) -> None:
        self.id = number
        self.user_id = user.pk
        self.challenge_id = challenge_id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.start = session.start
        self.end = session.end
        self.is_finished = is_finished
        if len(user_answers) != 0:
            self.true_answer = sum(
                [1 if answer.is_true else 0 for answer in user_answers]
            )
            self.false_answer = sum(
                [0 if answer.is_true else 1 for answer in user_answers]
            )
            self.percent = round(
                (self.true_answer / (self.true_answer + self.false_answer)) * 100
            )
        else:
            self.true_answer = 0
            self.false_answer = 0
            self.percent = 0
