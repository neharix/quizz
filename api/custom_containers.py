class ChallengeContainer:
    def __init__(
        self, pk: int, name: str, time: int, question_count: int, is_participated: bool
    ) -> None:
        self.pk = pk
        self.name = name
        self.time_for_event = time
        self.question_count = question_count
        self.is_participated = is_participated
