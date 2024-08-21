import flet as ft
from flet import Container, ControlEvent, KeyboardEvent, Page, Row, Text, border, colors


def main(page: Page):

    def build_dialog(image_url: str):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        column = ft.Column(
            controls=[
                ft.Image(
                    src=f"http://127.0.0.1:8000{image_url}",
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

    def show_dlg(e):
        dlg = build_dialog("/media/answers/images.jpg")
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
