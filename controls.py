import flet as ft

import theme


def section_title(kicker: str, title: str, subtitle: str | None = None) -> ft.Column:
    controls: list[ft.Control] = [
        ft.Text(kicker.upper(), size=20, weight=ft.FontWeight.W_700, color=theme.BLUE),
        ft.Text(title, style=theme.title_style(24), text_align=ft.TextAlign.CENTER),
    ]
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
    def __init__(self, label: str, icon: str, on_click=None, primary=True, url=None):
        super().__init__()
        self.primary = primary
        self.content = ft.Row(
            [
                ft.Icon(icon, size=18, color=theme.WHITE),
                ft.Text(label, size=15, weight=ft.FontWeight.W_700, color=theme.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
            spacing=9,
        )
        self.padding = ft.Padding(22, 22, 22, 22)
        self.border_radius = ft.BorderRadius(
            top_left=1,
            top_right=1,
            bottom_left=1,
            bottom_right=1,
        )
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
        active = e.data == "true"
        self.scale = ft.Scale(1.035 if active else 1)
        if self.primary:
            self.gradient = None if active else self.default_gradient
            self.bgcolor = "#16A34A" if active else self.default_bgcolor
        self.shadow = None
        self.update()


class GlassCard(ft.Container):
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
        self.content = content
        self.padding = padding
        self.border_radius = ft.BorderRadius(
            top_left=1,
            top_right=1,
            bottom_left=1,
            bottom_right=1,
        )
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
        active = e.data == "true"
        self.scale = ft.Scale(1.025 if active else 1)
        self.border = ft.Border.all(1, ft.Colors.with_opacity(0.34 if active else 0.16, theme.WHITE))
        self.shadow = None
        self.update()


def max_width(content: ft.Control, width=None, padding=56) -> ft.Container:
    return ft.Container(
        content=content,
        width=width or float("inf"),
        padding=ft.Padding(padding, 0, padding, 0),
        alignment=ft.Alignment(0, 0),
    )
