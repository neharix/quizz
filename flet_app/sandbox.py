import flet as ft


def main(page: ft.Page):
    page.title = "Grid Try"

    list_name = ["hello", "bye"]

    page.update()


ft.app(main)
