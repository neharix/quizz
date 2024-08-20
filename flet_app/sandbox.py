import flet as ft
from flet import Container, ControlEvent, KeyboardEvent, Page, Row, Text, border, colors


def main(page: Page):

    column = ft.Column(
        controls=[
            ft.Image(
                src="http://127.0.0.1:8000/media/answers/images_girl_2js7Yu5.jpg",
                expand=True,
            ),
        ]
    )

    container = ft.Container(content=column, height=600)

    def build_dialog():
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            content=container,
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        dlg_modal.on_dismiss = lambda e: None

        return dlg_modal

    def show_dlg(e):
        dlg = build_dialog()
        dlg.open = True
        page.overlay.append(dlg)
        page.update()

    main_container = ft.Container(
        on_click=lambda e: print("I'm working"),
        bgcolor=ft.colors.SECONDARY_CONTAINER,
        border_radius=30,
        padding=15,
        data=1,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("answer"),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=show_dlg),
            ],
            scroll=ft.ScrollMode.AUTO,
        ),
        shadow=ft.BoxShadow(1, 7.5, "#e2e2e2"),
        animate=ft.animation.Animation(150, ft.AnimationCurve.EASE_IN),
    )

    page.add(main_container)


ft.app(target=main)
