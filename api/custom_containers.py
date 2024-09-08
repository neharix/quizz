from django.contrib.auth.models import User

from challenge.models import TestSession


class ChallengeContainer:
    def __init__(
        self, pk: int, name: str, time: int, question_count: int, is_participated: bool
    ) -> None:
        self.pk = pk
        self.name = name
        self.time_for_event = time
        self.question_count = question_count
        self.is_participated = is_participated


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
        self.start = session.start.strftime("%d.%m.%Y %H:%M:%S")
        self.end = session.end.strftime("%d.%m.%Y %H:%M:%S")
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
