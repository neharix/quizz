import random

import components
import flet as ft
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
        self.__challenge_data = requests.request(
            "GET", f"{settings.API_URL}/api/v1/challenge/{self.__challenge_pk}/", headers={"Authorization": self.__token}
        ).json()

        questions_data = requests.request(
            "GET", f"{settings.API_URL}/api/v1/challenge-data/{self.__challenge_pk}/", headers={"Authorization": self.__token}
        ).json()
        random.shuffle(questions_data)
        self.__questions_menu = components.QuestionsMenu(
            [components.Question(question) for question in questions_data]
        )
        self.current_question_index = 0

        self.route = "/challenge"

        self.__quizz_panel = ft.Column(scroll=ft.ScrollMode.AUTO)

        self.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ARROW_FORWARD, scale=1.1, width=110, height=45, on_click=lambda e: print("Hello"), bgcolor=ft.colors.PRIMARY, foreground_color=ft.colors.WHITE)


        self.__question_row = ft.Row(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.INVERSE_PRIMARY, 
                    content=ft.Row(
                        controls=[
                            ft.Text
                            (
                                self.__questions_menu.controls[0].question, 
                                expand=True,
                                size=18,
                            )
                        ],
                    ),
                    expand=True,
                    margin=ft.margin.only(10, 20, 10, 25),
                    padding=ft.padding.only(20, 15, 20, 15),
                    shadow=ft.BoxShadow(1, 10, "#bdbdbd"),
                    border_radius=30,
                ),
            ],
        )
        
        self.__answers_grid = ft.GridView(auto_scroll=True, runs_count=2, padding=10, height=295, child_aspect_ratio=5)
        
        self.__answer_containers = [
            ft.Container(
                on_click=self.__select,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                border_radius=30,
                padding=15,
                data=i,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Text("answer"),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(1, 7.5, "#e2e2e2"),
                animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_IN)
            )
            for i in range(3)
        ]
        self.__answer_containers.append(
            ft.Container(
                on_click=self.__select,
                bgcolor=ft.colors.SECONDARY_CONTAINER,
                border_radius=30,
                padding=15,
                data=3,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    expand=True,
                    controls=[
                        ft.Text("image"),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda e: print("It's me\n")),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
                shadow=ft.BoxShadow(1, 7.5, "#e2e2e2"),
                animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_IN),
            )
        )
        self.__selected_answer = None

        for container in self.__answer_containers:
            self.__answers_grid.controls.append(container)
        
        self.__quizz_panel.controls = [
            self.__question_row, 
            ft.Row(controls=[ft.Text("Jogaplar:", size=18)]),
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
                            ft.ProgressRing(
                                value=1,
                            ),
                            ft.Text(
                                f"0/{self.__challenge_data["question_count"]}   ")
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
