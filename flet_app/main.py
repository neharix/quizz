import asyncio
import random
import threading
import time

import flet as ft
import requests

api_url = "http://127.0.0.1:8000"

token = ""


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
            self.value = "{:02d}:{:02d}".format(mins, secs)
            self.update()
            await asyncio.sleep(1)
            self.seconds -= 1


def main(page: ft.Page):

    # Функционал и компоненты страницы входа
    def build_dialog(dialog_title, dialog_message):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

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

    def submit(e):
        global token

        name = name_field.value
        surname = surname_field.value
        about = about_field.value

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
            dlg_modal = build_dialog(dialog_title, dialog_message)
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            page.update()
        elif name == "" or surname == "":
            dialog_title = "Doly giriziň!"
            if name == "" and surname == "":
                dialog_message = "Adyňyzy we familiýaňyzy girizmegiňizi haýyş edýäris!"
            elif name == "" and not surname == "":
                dialog_message = "Adyňyzy girizmegiňizi haýyş edýäris!"
            elif surname == "" and not name == "":
                dialog_message = "Familiýaňyzy girizmegiňizi haýyş edýäris!"
            dlg_modal = build_dialog(dialog_title, dialog_message)
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            page.update()
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
                user_url = f"{api_url}/api/v1/auth/users/"
                journal_url = f"{api_url}/api/v1/auth-journal/create"
                login_url = f"{api_url}/api/v1/auth/token/login"

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
                    url = f"{api_url}/api/v1/auth-journal/" + username
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
                        f"{api_url}/api/v1/create_profile/",
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
                token = "Token " + login_response["auth_token"]
                page.go("/challenges")
            except requests.exceptions.ConnectionError:
                dialog_title = "Baglanyşyk näsazlygy"
                dialog_message = "Serwer bilen baglanyşyk prosesinde näsazlyk döredi. Internet/Ethernet baglanyşygyňyzy barlaň!"
                dlg_modal = build_dialog(dialog_title, dialog_message)
                page.overlay.append(dlg_modal)
                dlg_modal.open = True
                page.update()

    name_field = ft.TextField(
        label="Ady",
        border_color=ft.colors.WHITE,
        focused_color=ft.colors.BLACK87,
        hover_color=ft.colors.WHITE24,
        fill_color=ft.colors.WHITE24,
    )
    surname_field = ft.TextField(
        label="Familiýasy",
        border_color=ft.colors.WHITE,
        focused_color=ft.colors.BLACK87,
        hover_color=ft.colors.WHITE24,
        fill_color=ft.colors.WHITE24,
    )
    about_field = ft.TextField(
        label="Edarasy",
        border_color=ft.colors.WHITE,
        focused_color=ft.colors.BLACK87,
        hover_color=ft.colors.WHITE24,
        selection_color=ft.colors.WHITE12,
        fill_color=ft.colors.WHITE24,
    )
    submit_btn = ft.ElevatedButton("Tassyklamak", on_click=submit)

    column = ft.Column(
        [
            ft.Row([name_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([surname_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([about_field], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([submit_btn], alignment=ft.MainAxisAlignment.END),
        ],
        spacing=20,
    )
    container = ft.Container(
        column,
        bgcolor=ft.colors.BLUE_100,
        width=400,
        padding=ft.padding.all(40),
        border_radius=10,
        margin=ft.margin.only(top=150, bottom=150),
        shadow=ft.BoxShadow(1, 10, "#878787"),
    )

    login_container = ft.Container(container, alignment=ft.alignment.center)

    # функционал и компоненты страницы выбора теста

    def run_challenge(pk: int):
        global challenge_data

        challenge_data = requests.request(
            "GET", f"{api_url}/api/v1/challenge/{pk}/", headers={"Authorization": token}
        ).json()

        page.go("/challenge")

    def build_challenges_grid_view():

        challenges_list = requests.request(
            "GET", f"{api_url}/api/v1/challengelist/", headers={"Authorization": token}
        ).json()

        grid = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=300,
            child_aspect_ratio=3,
            spacing=10,
            run_spacing=10,
        )

        containers = [
            ft.Container(
                on_click=lambda e: run_challenge(challenge["pk"]),
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
                                ft.Text(f"Sorag sany: {challenge['question_count']}"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                ),
            )
            for challenge in challenges_list
        ]

        for container in containers:
            grid.controls.append(container)

        return grid

    # функционал и компоненты страницы викторины

    # Параметры страницы

    def route_change(e):
        global timer_label
        timer_label = ft.PopupMenuItem(text="Galan wagt:")

        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(
                        title=ft.Text("Giriş"),
                        center_title=True,
                        bgcolor=ft.colors.SURFACE_VARIANT,
                    ),
                    login_container,
                ],
            )
        )
        if page.route == "/challenges":
            page.views.append(
                ft.View(
                    "/challenges",
                    [
                        ft.AppBar(
                            title=ft.Text("Testler"),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            center_title=True,
                        ),
                        build_challenges_grid_view(),
                    ],
                )
            )

        if page.route == "/challenge":
            page.views.append(
                ft.View(
                    "/challenge",
                    [
                        ft.AppBar(
                            title=ft.Text(challenge_data["name"]),
                            bgcolor=ft.colors.SURFACE_VARIANT,
                            center_title=True,
                            actions=[
                                ft.Row(
                                    controls=[
                                        ft.Icon(ft.icons.TIMER_SHARP),
                                        CountDownText(challenge_data["time_for_event"]),
                                    ],
                                )
                            ],
                        ),
                    ],
                )
            )

        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.title = "IT Meydança Quiz"
    page.window.maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.update()
    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


ft.app(target=main)
