import os
from pathlib import Path

import flet as ft

import theme
from landing import LandingPage


# Pasta raiz do projeto. O Flet usa esse caminho para encontrar imagens,
# index.html, manifest.json e arquivos da abertura personalizada.
PROJECT_DIR = Path(__file__).resolve().parent


def main(page: ft.Page):
    """Configura a janela/pagina principal e carrega a landing page."""

    # Titulo que aparece na aba do navegador.
    page.title = "SmartLuup | Tecnologia Inteligente"

    # Icone usado na janela/app. A tela de abertura web usa o index.html.
    page.window.icon = "logonovosmartluup.png"

    # Configuracoes gerais de aparencia e comportamento da pagina.
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0950C2"
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO
    page.window.min_width = 390
    page.window.min_height = 760

    # Fonte principal do site. Os numeros indicam pesos: normal, semibold,
    # negrito, extra bold e black.
    page.fonts = {
        "Inter": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap"
    }
    page.theme = ft.Theme(font_family="Inter", color_scheme_seed=theme.BLUE)

    # Cria a pagina de landing, adiciona na tela e inicia animacoes.
    landing = LandingPage(page)
    page.add(landing.build())
    page.update()
    landing.start_animations()


if __name__ == "__main__":
    # No Render a porta vem pela variavel PORT. Localmente usa 8088.
    port = int(os.getenv("PORT", "8088"))

    # No Render precisa aceitar conexoes externas em 0.0.0.0.
    # Localmente fica em 127.0.0.1.
    host = os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")

    # Inicia o servidor web do Flet.
    ft.run(
        main,
        assets_dir=str(PROJECT_DIR),
        host=host,
        port=port,
        view=ft.AppView.WEB_BROWSER,
    )
