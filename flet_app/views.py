import datetime
import random
from typing import List

import components
import flet as ft
import pytz
import requests
import settings


class LoginPage(ft.View):

    def __init__(self):
        super().__init__()
        self.route = "/"

        self.__name_field = ft.TextField(
            label="Ady",
            border_color=ft.colors.WHITE,
            focused_color=ft.colors.BLACK87,
            hover_color=ft.colors.WHITE24,
            fill_color=ft.colors.WHITE24,
        )
        self.__surname_field = ft.TextField(
            label="Familiýasy",
            border_color=ft.colors.WHITE,
            focused_color=ft.colors.BLACK87,
            hover_color=ft.colors.WHITE24,
            fill_color=ft.colors.WHITE24,
        )
        self.__about_field = ft.TextField(
            label="Edarasy",
            border_color=ft.colors.WHITE,
            focused_color=ft.colors.BLACK87,
            hover_color=ft.colors.WHITE24,
            selection_color=ft.colors.WHITE12,
            fill_color=ft.colors.WHITE24,
        )
        self.__submit_btn = ft.ElevatedButton(
            "Tassyklamak", on_click=lambda e: self.__submit()
        )
        self.__column = ft.Column(
            [
                ft.Row([self.__name_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.__surname_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.__about_field], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([self.__submit_btn], alignment=ft.MainAxisAlignment.END),
            ],
            spacing=20,
        )
        self.__appbar = ft.AppBar(
            title=ft.Text("Giriş"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )

        self.__login_container = ft.Container(
            ft.Container(
                self.__column,
                bgcolor=ft.colors.INVERSE_PRIMARY,
                width=400,
                padding=ft.padding.all(40),
                border_radius=10,
                margin=ft.margin.only(top=150, bottom=150),
                shadow=ft.BoxShadow(1, 10, "#bdbdbd"),
            ),
            alignment=ft.alignment.center,
        )
        self.controls = [self.__appbar, self.__login_container]
        self.__about_field_focused = False

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

        return dlg_modal

    def __submit(self):

        name = self.__name_field.value
        surname = self.__surname_field.value
        about = self.__about_field.value

        cyrillic = "ёйцукенгшщзхъфывапролджэячсмитьбю"
        symbols = ".,/\\`'[]()!@#$%^&*№:;{}<>?+=-_" + '"'
        filling_error = False
        for char in name.lower() + surname.lower() + about.lower():
            if char in symbols or char in cyrillic:
                filling_error = True
                break

        if filling_error:
            dialog_title = "Kabul edilmeýän simwollar"
            dialog_message = "Girizen maglumatlaryňyzda kabul edilmeýän simwollar ulanylypdyr! Täzeden synanyşmagyňyzy haýyş edýäris!"
            dlg_modal = self.__build_dialog(dialog_title, dialog_message)
            self.page.overlay.append(dlg_modal)
            dlg_modal.open = True
            self.page.update()
        elif name == "" or surname == "":
            dialog_title = "Doly giriziň!"
            if name == "" and surname == "":
                dialog_message = "Adyňyzy we familiýaňyzy girizmegiňizi haýyş edýäris!"
            elif name == "" and not surname == "":
                dialog_message = "Adyňyzy girizmegiňizi haýyş edýäris!"
            elif surname == "" and not name == "":
                dialog_message = "Familiýaňyzy girizmegiňizi haýyş edýäris!"
            dlg_modal = self.__build_dialog(dialog_title, dialog_message)
            self.page.overlay.append(dlg_modal)
            dlg_modal.open = True
            self.page.update()
        else:
            enable_chars = ("qwertyuiopasdfghjklzxcvbnm", "1234567890")
            password = ""
            username = (
                (name + surname)
                .lower()
                .replace("ý", "y")
                .replace("ž", "zh")
                .replace("ä", "a")
                .replace("ç", "ch")
                .replace("ş", "sh")
                .replace("ň", "n")
                .replace("ö", "o")
                .replace("ü", "u")
            )
            for i in range(random.randint(8, 12)):
                in_choice = random.randint(0, 1)
                if in_choice == 0:
                    letter_id = random.randint(0, 25)
                    password += random.choice(
                        (
                            enable_chars[0][letter_id].upper(),
                            enable_chars[0][letter_id].lower(),
                        )
                    )
                else:
                    password += enable_chars[1][random.randint(0, 9)]
            try:
                user_url = f"{settings.API_URL}/api/v1/auth/users/"
                journal_url = f"{settings.API_URL}/api/v1/auth-journal/create"
                login_url = f"{settings.API_URL}/api/v1/auth/token/login"

                payload = {
                    "first_name": name,
                    "last_name": surname,
                    "username": username,
                    "password": password,
                    "email": "stub@email.com",
                }
                payload_dub = {
                    "name": name,
                    "surname": surname,
                    "username": username,
                    "password": password,
                }

                files = []
                headers = {}

                user_response = requests.request(
                    "POST", user_url, headers=headers, data=payload, files=files
                ).json()

                if (
                    user_response["username"][0]
                    == "A user with that username already exists."
                    or user_response["username"][0]
                    == "Пользователь с таким именем уже существует."
                ):
                    url = f"{settings.API_URL}/api/v1/auth-journal/" + username
                    response = requests.request(
                        "GET", url, headers=headers, files=files
                    ).json()
                    login_payload = {
                        "username": response[0]["username"],
                        "password": response[0]["password"],
                    }
                else:

                    profile_payload = {
                        "about": about if about != "" else "Default",
                        "user": user_response["id"],
                    }

                    profile_response = requests.request(
                        "POST",
                        f"{settings.API_URL}/api/v1/create_profile/",
                        headers={},
                        data=profile_payload,
                    ).json()

                    response = requests.request(
                        "POST",
                        journal_url,
                        headers=headers,
                        data=payload_dub,
                        files=files,
                    ).json()
                    login_payload = {
                        "username": response["username"],
                        "password": response["password"],
                    }

                login_response = requests.request(
                    "POST", login_url, headers=headers, data=login_payload, files=files
                ).json()
                self.__token = "Token " + login_response["auth_token"]
                self.page.go("/challenges")
            except requests.exceptions.ConnectionError:
                dialog_title = "Baglanyşyk näsazlygy"
                dialog_message = "Serwer bilen baglanyşyk prosesinde näsazlyk döredi. Internet/Ethernet baglanyşygyňyzy barlaň!"
                dlg_modal = self.__build_dialog(dialog_title, dialog_message)
                self.page.overlay.append(dlg_modal)
                dlg_modal.open = True
                self.page.update()

    def get_token(self):
        return self.__token

    def focus(self, e: ft.KeyboardEvent):

        if e.key == "Enter":
            fields = (self.__name_field, self.__surname_field) if self.__about_field_focused else (self.__name_field, self.__surname_field, self.__about_field)
            blank_filled = True
            for field in fields:
                if field.value == "":
                    self.__about_field_focused = True if fields.index(field) == 2 else False
                    blank_filled = False
                    field.focus()
                    break
            if blank_filled:
                self.__submit()


        self.page.update()

class ChallengesPage(ft.View):
    def __init__(self, token: str):
        super().__init__()
        self.__token = token
        self.__challenges_list = requests.request(
            "GET", f"{settings.API_URL}/api/v1/challengelist/", headers={"Authorization": self.__token}
        ).json()

        self.__appbar = ft.AppBar(
            title=ft.Text("Testler"),
            bgcolor=ft.colors.SURFACE_VARIANT,
            center_title=True,
        )

        self.__grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=3,
            spacing=10,
            run_spacing=10,
        )

        containers = [
            ft.Container(
                on_click=lambda e: self.__run_challenge(pk=e.control.data),
                data=challenge["pk"],
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                border_radius=5,
                padding=15,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Icon(name=ft.icons.QUIZ_OUTLINED),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    challenge["name"],
                                    weight=ft.FontWeight.W_500,
                                    size=20,
                                ),
                                ft.Text(f"Sorag sany: {
                                        challenge['question_count']}"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
            )
            for challenge in self.__challenges_list
        ]

        for container in containers:
            self.__grid.controls.append(container)

        self.controls = [
            self.__appbar,
            self.__grid,
        ]


    def __run_challenge(self, pk: int):

        self.__selected_challenge = pk

        self.page.go("/challenge")

    def get_selected_challenge(self):
        return self.__selected_challenge

class ChallengePage(ft.View):
    def __init__(self, pk: int, token: str):
        super().__init__()
        self.__token = token
        self.__challenge_pk = pk
        self.__user_data = requests.request(
            "GET",
            f"{settings.API_URL}/api/v1/auth/users/",
            headers={"Authorization": self.__token},
        ).json()
        self.__challenge_data = requests.request(
            "GET", f"{settings.API_URL}/api/v1/challenge/{self.__challenge_pk}/", headers={"Authorization": self.__token}
        ).json()
        self.__session = requests.request(
            "POST",
            url=f"{settings.API_URL}/api/v1/test-session-create/",
            headers={"Authorization": self.__token},
            data={"challenge": self.__challenge_pk, "user": int(self.__user_data[0]["id"])},
        ).json()

        questions_data = requests.request(
            "GET", f"{settings.API_URL}/api/v1/challenge-data/{self.__challenge_pk}/", headers={"Authorization": self.__token}
        ).json()
        random.shuffle(questions_data)
        self.__questions_menu: components.QuestionsMenu = components.QuestionsMenu(
            [components.Question(question) for question in questions_data], self.__question_menu_item_clicked,
        )

        self.__requests_quene = components.RequestsQuene(settings.API_URL, {"Authorization": self.__token})

        self.route = "/challenge"

        self.__quizz_panel = ft.Column(scroll=ft.ScrollMode.AUTO)

        self.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ARROW_FORWARD, scale=1.1, width=110, height=45, on_click=self.__accept, bgcolor=ft.colors.PRIMARY, foreground_color=ft.colors.WHITE)

        self.__current_question_index = 0
        question: components.Question = self.__questions_menu.controls[self.__current_question_index].question

        if question.is_image:
            row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[
                    ft.Text("Suraty görmek üçin basyň", weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, data=question.image, on_click=self.__show_image_dialog),
                ],
                spacing=10,
            )
        else:
            row = ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(question.question),
                ],
                scroll=ft.ScrollMode.AUTO,
            )

        self.__question_row = ft.Row(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.INVERSE_PRIMARY, 
                    content=row,
                    expand=True,
                    margin=ft.margin.only(10, 20, 10, 25),
                    padding=ft.padding.only(20, 15, 20, 15),
                    shadow=ft.BoxShadow(1, 10, "#bdbdbd"),
                    border_radius=30,
                ),
            ],
        )
        
        self.__answers_grid = ft.GridView(auto_scroll=True, runs_count=2, padding=10, height=295, child_aspect_ratio=5)
        
        self.__answer_containers = self.__build_answer_containers(self.__questions_menu.controls[0].question.answers)
        self.__selected_answer = None
        self.__current_question = question.pk
        self.__answered_questions_count = 0
        self.__progress_ring = ft.ProgressRing(value=1)
        self.__answered_questions_count_text = ft.Text(f"{self.__answered_questions_count}/{self.__challenge_data["question_count"]}   ")

        self.__answers_grid.controls = self.__answer_containers
        
        self.__quizz_panel.controls = [
            ft.Row(controls=[ft.Text("Sorag:", size=18)], alignment=ft.MainAxisAlignment.CENTER),
            self.__question_row, 
            ft.Row(controls=[ft.Text("Jogaplar:", size=18)], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(
                content=self.__answers_grid,
                margin=ft.margin.only(top=25)
            )
        ]

        self.controls = [
            ft.AppBar(
                title=ft.Text(self.__challenge_data["name"]),
                bgcolor=ft.colors.SURFACE_VARIANT,
                center_title=True,
                actions=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.icons.TIMER_SHARP),
                            components.CountDownText(
                                self.__challenge_data["time_for_event"]),
                        ],
                    ),
                    ft.Row(
                        controls=[
                            self.__progress_ring,
                            self.__answered_questions_count_text,
                        ],
                    )
                ],
            ),
            ft.Row(
                controls=[
                    ft.Container(content=self.__questions_menu, alignment=ft.alignment.top_center),
                    ft.VerticalDivider(),
                    ft.Container(content=self.__quizz_panel, expand=True, alignment=ft.alignment.top_center),
                ],    
                expand=True,
                spacing=10,
                alignment=ft.alignment.top_center,
            )
        ]

    
    def __build_image_dialog(self, image_url: str):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        column = ft.Column(
            controls=[
                ft.Image(
                    src=f"{settings.API_URL}{image_url}",
                    expand=True,
                ),
            ]
        )

        container = ft.Container(content=column, height=600)

        dlg_modal = ft.AlertDialog(
            modal=True,
            content=container,
            actions=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.START,
        )
        return dlg_modal

    def __show_image_dialog(self, e: ft.ControlEvent):
        dlg = self.__build_image_dialog(e.control.data)
        dlg.open = True
        self.page.overlay.append(dlg)
        self.page.update()


    def __build_answer_containers(self, answers: List[components.Answer]):
        containers = []

        for answer in answers:
            if answer.is_image:
                row = ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    controls=[
                        ft.Text("Suraty görmek üçin basyň", weight=ft.FontWeight.BOLD, color=ft.colors.PRIMARY),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, data=answer.image, on_click=self.__show_image_dialog),
                    ],
                    spacing=10,
                )
            else:
                row = ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Text(answer.answer, color=ft.colors.PRIMARY),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                )
            containers.append(
                ft.Container(
                    on_click=self.__select,
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    border_radius=30,
                    padding=15,
                    data=answer,
                    content=row,
                    shadow=ft.BoxShadow(1, 7.5, "#e2e2e2"),
                    animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_IN)
                )
            )
        return containers

    def __select(self, e: ft.ControlEvent):
        for answer_container in self.__answer_containers:
        
            if answer_container.data != e.control.data:
                answer_container.bgcolor = ft.colors.SECONDARY_CONTAINER
            else:
                if self.__selected_answer == e.control.data:
                    self.__selected_answer = None
                    answer_container.bgcolor = ft.colors.SECONDARY_CONTAINER
                else:
                    self.__selected_answer = answer_container.data
                    answer_container.bgcolor = ft.colors.INVERSE_PRIMARY
        self.page.update()

    def __accept(self, e: ft.ControlEvent):
        print(self.__selected_answer)
        if self.__selected_answer == None and e.control.data != "modal_accept":
            self.__dlg_empty_answer_modal = self.__build_empty_answer_dialog("Jogap meýdançasy boş!", "Dowam eden ýagdaýyňyzda soragy bilmedigiňizi tassyklarsyňyz.")
            self.page.overlay.append(self.__dlg_empty_answer_modal)
            self.__dlg_empty_answer_modal.open = True
            self.page.update()
        else:
            if e.control.data == "modal_accept":
                self.__dlg_empty_answer_modal.open = False
            self.__questions_menu.controls[self.__current_question_index].question.is_answered = True
            try:
                index = self.__current_question_index + 1
                if not self.__questions_menu.controls[index].question.is_answered:
                    self.__current_question_index += 1
                else:
                    # не бейте палками. лень новое исключение создавать
                    raise IndexError
            except IndexError:
                for item in self.__questions_menu.controls:
                    if not item.question.is_answered:
                        self.__current_question_index = self.__questions_menu.controls.index(item)
                        break
                else:
                    # TODO Create Chart View
                    pass
            payload = {
                "answer": None if self.__selected_answer == None else self.__selected_answer.pk,
                "question": self.__current_question,
                "user": self.__user_data[0]["id"],
                "datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            self.__questions_menu.selected_index = self.__current_question_index
            self.__questions_menu.update_selected_item()
            self.__answered_questions_count += 1
            self.__progress_ring.value = 1 - (self.__answered_questions_count / self.__challenge_data["question_count"])
            self.__answered_questions_count_text.value = f"{self.__answered_questions_count}/{self.__challenge_data["question_count"]}   "
            self.__update_page()
            self.__requests_quene.send(payload)
            self.__selected_answer = None

    def __question_menu_item_clicked(self, e):
        self.__current_question_index = e.control.data
        self.__questions_menu.selected_index = e.control.data
        self.__questions_menu.update_selected_item()
        self.__update_page()
        self.__selected_answer = None

    def __update_page(self):
        question: components.Question = self.__questions_menu.controls[self.__current_question_index].question
        self.__current_question = question.pk
        if question.is_image:
            row = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True,
                controls=[
                    ft.Text("Suraty görmek üçin basyň", weight=ft.FontWeight.BOLD),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, data=question.image, on_click=self.__show_image_dialog),
                ],
                spacing=10,
            )
        else:
            row = ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(question.question),
                ],
                scroll=ft.ScrollMode.AUTO,
            )

        self.__question_row = ft.Row(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.INVERSE_PRIMARY, 
                    content=row,
                    expand=True,
                    margin=ft.margin.only(10, 20, 10, 25),
                    padding=ft.padding.only(20, 15, 20, 15),
                    shadow=ft.BoxShadow(1, 10, "#bdbdbd"),
                    border_radius=30,
                ),
            ],
        )
        self.__quizz_panel.controls[1] = self.__question_row
        self.__answer_containers = self.__build_answer_containers(self.__questions_menu.controls[self.__current_question_index].question.answers)
        self.__answers_grid.controls = self.__answer_containers
        self.page.update()

    def __build_empty_answer_dialog(self, dialog_title, dialog_message):
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(dialog_title),
            content=ft.Text(dialog_message),
            actions=[
                ft.IconButton(icon=ft.icons.HIGHLIGHT_OFF, on_click=close_dlg),
                ft.IconButton(icon=ft.icons.CHECK_CIRCLE_OUTLINE, on_click=self.__accept, data="modal_accept"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        return dlg_modal
