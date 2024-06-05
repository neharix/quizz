from django.contrib.auth.models import User

from challenge.models import Challenge


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


class UserResult:
    def __init__(self, number: int, user: User, user_answers: list) -> None:
        self.id = number
        self.first_name = user.first_name
        self.last_name = user.last_name
        if len(user_answers) != 0:
            self.answered_at = user_answers[len(user_answers) - 1].answered_at
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
            self.answered_at = None
            self.true_answer = 0
            self.false_answer = 0
            self.percent = 0
