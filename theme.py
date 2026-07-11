import flet as ft


BG = "#0F172A"
PANEL = "#1E293B"
BLUE = "#3B82F6"
PURPLE = "#8B5CF6"
WHITE = "#FFFFFF"
MUTED = "#94A3B8"
CYAN = "#22D3EE"
GREEN = "#34D399"
PINK = "#EC4899"
AMBER = "#F59E0B"


def gradient(colors=None):
    return ft.LinearGradient(
        begin=ft.Alignment(-1, -1),
        end=ft.Alignment(1, 1),
        colors=colors or ["#0950C2"],
    )


def soft_shadow(color="#0950C2", opacity=0.5, blur=30, spread=0):
    return [
        ft.BoxShadow(
            blur_radius=blur,
            spread_radius=spread,
            color=ft.Colors.with_opacity(opacity, color),
            offset=ft.Offset(10, 18),
        )
    ]


def glass_bg(opacity=0.55):
    return ft.Colors.with_opacity(opacity, PANEL)


def title_style(size=42):
    return ft.TextStyle(
        size=size,
        weight=ft.FontWeight.W_800,
        color=WHITE,
        height=1.04,
    )


def body_style(size=16, color=MUTED):
    return ft.TextStyle(size=size, color=color, height=1.5)
