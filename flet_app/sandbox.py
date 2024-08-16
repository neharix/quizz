import flet as ft
from flet import Container, ControlEvent, KeyboardEvent, Page, Row, Text, border, colors


class ButtonControl(Container):
    def __init__(self, text):
        super().__init__()
        self.content = Text(text)
        self.border = border.all(1, colors.BLACK54)
        self.border_radius = 3
        self.bgcolor = "0x09000000"
        self.padding = 10
        self.visible = False


def main(page: Page):

    column = ft.Column(
        controls=[
            ft.Image(
                src="http://127.0.0.1:8000/media/answers/images_girl_2js7Yu5.jpg",
                expand=True,
            ),
            ft.ElevatedButton("Hello", on_click=lambda e: print(e.control.text)),
        ]
    )

    container = ft.Container(content=column, height=600)

    def bs_dismissed(e):
        print("Dismissed!")

    def show_bs(e):
        bs.open = True
        bs.update()

    def close_bs(e):
        bs.open = False
        bs.update()

    bs = ft.AlertDialog(
        title=ft.Text(""),
        content=container,
        open=True,
        on_dismiss=bs_dismissed,
        actions=[],
    )
    page.overlay.append(bs)
    page.add(ft.ElevatedButton("Display bottom sheet", on_click=show_bs))


ft.app(target=main)
