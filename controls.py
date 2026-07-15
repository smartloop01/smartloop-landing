import flet as ft

import theme


def section_title(kicker: str, title: str, subtitle: str | None = None) -> ft.Column:
    """Monta o titulo padrao de cada secao da landing."""

    # Lista base: texto pequeno de categoria + titulo principal.
    controls: list[ft.Control] = []
    if kicker:
        controls.append(ft.Text(kicker.upper(), size=20, weight=ft.FontWeight.W_700, color=theme.BLUE))
    controls.append(ft.Text(title, style=theme.title_style(24), text_align=ft.TextAlign.CENTER))

    # Subtitulo opcional. Use quando quiser explicar melhor a secao.
    if subtitle:
        controls.append(
            ft.Text(
                subtitle,
                style=theme.body_style(16),
                text_align=ft.TextAlign.CENTER,
                width=760,
            )
        )

    return ft.Column(
        controls=controls,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=8,
    )


class GlowButton(ft.Container):
    """Botao reutilizavel com icone, animacao de hover e link opcional."""

    def __init__(self, label: str, icon: str, on_click=None, primary=True, url=None):
        super().__init__()
        self.primary = primary

        # Conteudo visual do botao: icone + texto.
        self.content = ft.Row(
            [
                ft.Icon(icon, size=18, color=theme.WHITE),
                ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=theme.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
            spacing=9,
        )

        # Aparencia padrao do botao.
        self.padding = ft.Padding(22, 22, 22, 22)
        self.border_radius = ft.BorderRadius(
            top_left=14,
            top_right=14,
            bottom_left=14,
            bottom_right=14,
        )

        # Botoes primarios usam gradiente; secundarios usam fundo translucido.
        self.default_gradient = theme.gradient() if primary else None
        self.default_bgcolor = None if primary else ft.Colors.with_opacity(0.10, theme.BLUE)
        self.gradient = self.default_gradient
        self.bgcolor = self.default_bgcolor
        self.border = None if primary else ft.Border.all(1, ft.Colors.with_opacity(0.10,theme.BLUE))
        self.shadow = None
        self.animate = ft.Animation(260, ft.AnimationCurve.EASE_OUT)
        self.animate_scale = ft.Animation(220, ft.AnimationCurve.EASE_OUT)
        self.scale = ft.Scale(1)
        self.on_hover = self._hover
        self.on_click = on_click
        self.url = url

    def _hover(self, e: ft.ControlEvent):
        """Efeito quando o mouse passa por cima do botao."""

        active = e.data == "true"
        self.scale = ft.Scale(1.035 if active else 1)
        if self.primary:
            self.gradient = None if active else self.default_gradient
            self.bgcolor = "#16A34A" if active else self.default_bgcolor
        self.shadow = None
        self.update()


class GlassCard(ft.Container):
    """Card reutilizavel com visual de vidro e leve animacao no hover."""

    def __init__(
        self,
        content: ft.Control,
        padding=24,
        radius=28,
        expand=False,
        gradient_colors=None,
        on_click=None,
    ):
        super().__init__()

        # Conteudo que sera exibido dentro do card.
        self.content = content
        self.padding = padding

        # Bordas do card. Alterar estes valores muda o arredondamento.
        self.border_radius = ft.BorderRadius(
            top_left=18,
            top_right=18,
            bottom_left=18,
            bottom_right=18,
        )

        # Fundo e gradiente criam o efeito glassmorphism.
        self.bgcolor = theme.glass_bg()
        self.gradient = ft.LinearGradient(
            begin=ft.Alignment(-1, -1),
            end=ft.Alignment(1, 1),
            colors=gradient_colors
            or [
                ft.Colors.with_opacity(0.20, theme.BLUE),
                ft.Colors.with_opacity(0.08, theme.BLUE),
                ft.Colors.with_opacity(0.08, theme.BLUE),
            ],
        )
        self.border = ft.Border.all(2, ft.Colors.with_opacity(0.16, theme.WHITE))
        self.shadow = None
        self.animate = ft.Animation(260, ft.AnimationCurve.EASE_OUT)
        self.animate_scale = ft.Animation(220, ft.AnimationCurve.EASE_OUT)
        self.scale = ft.Scale(1)
        self.expand = expand
        self.on_hover = self._hover
        self.on_click = on_click

    def _hover(self, e: ft.ControlEvent):
        """Aumenta levemente o card quando o mouse passa por cima."""

        active = e.data == "true"
        self.scale = ft.Scale(1.025 if active else 1)
        self.border = ft.Border.all(1, ft.Colors.with_opacity(0.34 if active else 0.16, theme.WHITE))
        self.shadow = None
        self.update()


def max_width(content: ft.Control, width=None, padding=56) -> ft.Container:
    """Centraliza conteudo e aplica uma margem lateral padrao."""

    return ft.Container(
        content=content,
        width=width or float("inf"),
        padding=ft.Padding(padding, 0, padding, 0),
        alignment=ft.Alignment(0, 0),
    )
