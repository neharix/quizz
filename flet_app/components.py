import asyncio
import random

import flet as ft


class Answer:
    def __init__(self, answer: dict) -> None:
        self.pk = answer.get("pk")
        self.answer = answer.get("answer")
        self.question = answer.get("question")
        self.is_true = answer.get("is_true")
        self.image = answer.get("image")
        self.is_image = answer.get("is_image")


class Question:
    def __init__(self, question: dict) -> None:
        self.pk = question.get("pk")
        self.question = question.get("question")
        self.image = question.get("image")
        self.is_image = question.get("is_image")
        self.answers = []

        for answer in question.get("answers"):
            self.answers.append(Answer(answer))

        random.shuffle(self.answers)


class CountDownText(ft.Text):
    def __init__(self, minutes):
        super().__init__()
        self.seconds = minutes * 60

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    async def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            self.value = "{:02d}:{:02d}     ".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1
