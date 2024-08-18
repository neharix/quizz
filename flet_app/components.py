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


class NavigationItem(ft.Container):
    def __init__(self, question: Question, index, on_click):
        super().__init__()
        self.question = question
        self.ink = True
        self.padding = ft.padding.only(left=5, top=5, bottom=5, right=15)
        self.border_radius = 5
        self.icon = ft.Icon(
            name=ft.icons.QUESTION_MARK, color=ft.colors.PRIMARY, size=18
        )
        self.text = f"Sorag №{index}"
        self.content = ft.Row(
            controls=[
                self.icon,
                ft.Text(self.text),
            ],
            expand=True,
        )
        self.on_click = on_click


# FIXME
class QuestionsMenu(ft.Column):
    def __init__(self, questions: list) -> None:
        super().__init__()
        for index in range(len(questions)):
            self.controls.append(
                NavigationItem(questions[index], index + 1, lambda e: print(f"Clicked"))
            )
        self.scroll = ft.ScrollMode.ALWAYS


class CountDownText(ft.Text):
    def __init__(self, minutes):
        super().__init__()
        self.seconds = minutes * 60

    def did_mount(self):
        self.running = True
        self.page.run_task(self.update_timer)

    def will_unmount(self):
        self.running = False

    def __build_dialog(self, dialog_title, dialog_message):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(dialog_title),
            content=ft.Text(dialog_message),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        dlg_modal.on_dismiss = lambda e: self.page.window.close()

        return dlg_modal

    async def update_timer(self):
        while self.seconds and self.running:
            mins, secs = divmod(self.seconds, 60)
            hours, mins = divmod(mins, 60)
            if hours > 0:
                self.value = "{:02d}:{:02d}:{:02d}     ".format(hours, mins, secs)
            else:
                self.value = "{:02d}:{:02d}     ".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1
            if self.seconds == 0:
                self.value = "00:00     "
                close_modal = self.__build_dialog(
                    "Wagt doldy!",
                    "Test üçin berlen wagtyňyz doldy! Çykyşyňyzy tassyklaň!",
                )
                close_modal.open = True
                self.page.overlay.append(close_modal)
                self.page.update()


class QuizzPanel(ft.Container):
    quizz_column = ft.Column()
    question_container = ft.Container(bgcolor=ft.colors.PRIMARY_CONTAINER)
    data = quizz_column

    def __init__(self):
        super().__init__()

    def set_data(self, question: Question):
        if question.is_image:
            self.question_container.content = ft.Row(
                controls=[
                    ft.Text("Suraty görmek"),
                    ft.Icon(name=ft.icons.CHEVRON_RIGHT),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
            )
        else:
            self.question_container.content = ft.Text(question.question)

        self.quizz_column.controls.append(self.question_container)

    def update(self) -> None:
        self.quizz_column.update()
        self.question_container.update()
        return super().update()
