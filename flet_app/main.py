import random

import components
import flet as ft
import requests
import views

api_url = ""
token = ""


def main(page: ft.Page):
    global current_focus_position

    # Параметры страницы
    login_page = views.LoginPage()

    def route_change(e):
        global questions_menu, quizz_panel

        page.views.clear()
        page.views.append(login_page)
        if page.route == "/challenges":
            challenges_page = views.ChallengesPage(login_page.get_token())
            page.views.append(challenges_page)

        # if page.route == "/challenge":
        #     quizz_panel = components.QuizzPanel()
        #     page.views.append(
        #         ft.View(
        #             "/challenge",
        #             [
        #                 ft.AppBar(
        #                     title=ft.Text(challenge_data["name"]),
        #                     bgcolor=ft.colors.SURFACE_VARIANT,
        #                     center_title=True,
        #                     actions=[
        #                         ft.Row(
        #                             controls=[
        #                                 ft.Icon(ft.icons.TIMER_SHARP),
        #                                 components.CountDownText(
        #                                     challenge_data["time_for_event"]),
        #                             ],
        #                         ),
        #                         ft.Row(
        #                             controls=[
        #                                 ft.ProgressRing(
        #                                     value=1,
        #                                 ),
        #                                 ft.Text(
        #                                     f"0/{challenge_data["question_count"]}   ")
        #                             ],
        #                         )
        #                     ],
        #                 ),
        #                 ft.Row(controls=[
        #                     ft.Container(content=questions_menu,
        #                                  alignment=ft.alignment.top_center),
        #                     ft.VerticalDivider(),
        #                     quizz_panel,
        #                 ],
        #                     expand=True,
        #                     spacing=0,
        #                 )

        #             ],
        #         )
        #     )
        #     quizz_panel.set_data(questions_menu.controls[0].question)
        if page.route == "/":
            page.on_keyboard_event = login_page.focus
        else:
            page.on_keyboard_event = lambda e: None
        page.update()

        # if page.route == "/challenge":
        #     quizz_panel.update()

    # def focus(e: ft.KeyboardEvent):
    #     global current_focus_position

    #     if e.key == "Enter":
    #         if name_field.value == "" and current_focus_position == 0:
    #             name_field.focus()
    #         else:
    #             current_focus_position += 1
    #             if type(focus_subsequence[current_focus_position]) is ft.TextField:
    #                 focus_subsequence[current_focus_position].focus()
    #             else:
    #                 submit()
    #     page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        page.update()

    page.title = "IT Meydança Quiz"
    page.window.maximized = True
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    page.update()


ft.app(target=main)
