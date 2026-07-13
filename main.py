import os
from pathlib import Path

import flet as ft

import theme
from landing import LandingPage


def main(page: ft.Page):
    page.title = "SmartLoop | Tecnologia Inteligente"
    page.window.icon = "iniciosite.png"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0950C2"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.min_width = 390
    page.window.min_height = 760
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap"
    }
    page.theme = ft.Theme(font_family="Inter", color_scheme_seed=theme.BLUE)

    landing = LandingPage(page)
    page.add(landing.build())
    page.update()
    landing.start_animations()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8088"))
    host = os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    ft.run(
        main,
        assets_dir=str(Path(__file__).parent),
        host=host,
        port=port,
        view=ft.AppView.WEB_BROWSER,
    )
