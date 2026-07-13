from __future__ import annotations

import asyncio
import threading
import time
import inspect
import textwrap

import flet as ft

import theme
from config import CONTACT, PROJECTS, TESTIMONIALS
from controls import GlassCard, GlowButton, max_width, section_title
from ai_agent_service import ask_smartloop_ai
from lead_service import init_db, save_lead


SERVICE_CARDS = [
    ("smart_toy", "Automação RPA", "Robos que executam processos repetitivos com precisao."),
    ("language", "Desenvolvimento Web", "Sites, portais e sistemas rapidos para vender e operar melhor."),
    ("phone_iphone", "Aplicativos Mobile", "Apps mobile e web com experiencia fluida e escalavel."),
    ("psychology", "Inteligência Artificial", "IA aplicada para decisoes, atendimento e produtividade."),
    ("analytics", "Integraçâo de Sistemas", "Dados conectados entre plataformas, equipes e indicadores."),
    ("cloud_queue", "Soluções em Nuvem", "Arquiteturas seguras para crescer sem travar a operacao."),
]

DIFFERENTIALS = [
    ("bolt", "Entrega Rápida"),
    ("smart_toy", "Especialistas em IA"),
    ("sync", "Automação Inteligente"),
    ("trending_up", "Escalabilidade"),
    ("shield", "Segurança"),
    ("ads_click", "Soluções Sob Medida"),
]

METRICS = [
    ("Projetos", 50, "+", ""),
    ("Mil horas automatizadas", 100, "+", " mil"),
    ("Clientes", 30, "+", ""),
    ("Satisfacao", 98, "", "%"),
]


class LandingPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.metric_values: list[ft.Text] = []
        self.testimonial_index = 0
        init_db()
        self.testimonial_box = ft.AnimatedSwitcher(
            content=ft.Container(),
            duration=500,
            transition=ft.AnimatedSwitcherTransition.FADE,
        )
        self.agent_messages: list[tuple[str, str]] = [
            (
                "agent",
                "Ola! Sou o agente da SmartLoop. Pergunte sobre RPA, sites, apps, IA, ERP ou projetos sob medida.",
            )
        ]
        self.agent_messages_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.agent_input = ft.TextField(
            hint_text="Pergunte sobre a SmartLoop...",
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.65, theme.WHITE)),
            border_radius=8,
            multiline=True,
            min_lines=1,
            max_lines=3,
        )
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.SMART_TOY,
            tooltip="Agente IA SmartLoop",
            bgcolor=theme.GREEN,
            foreground_color=theme.WHITE,
            on_click=lambda _: self.show_ai_agent(),
        )

    def is_mobile(self) -> bool:
        return bool(self.page.width and self.page.width < 720)

    def build(self) -> ft.Control:
        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[theme.BG, "#08090C", "#0B090F", theme.BG],
            ),
            content=ft.Column(
                [
                    self.hero(),
                    self.services(),
                    self.about(),
                    self.portfolio(),
                    self.metrics(),
                    self.differentials(),
                    self.testimonials(),
                    self.final_cta(),
                    self.footer(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0,
            ),
        )

    def hero(self) -> ft.Control:
        mobile = self.is_mobile()
        logo_width = 330 if mobile else 700
        logo_height = 92 if mobile else 180
        hero_title_size = 31 if mobile else 48
        hero_body_size = 16 if mobile else 25
        hero_text_height = None if mobile else 430
        button_top_padding = 22 if mobile else 80
        dashboard_padding = 18 if mobile else 32
        dashboard_inner_width = 250 if mobile else 290
        dashboard_inner_height = 170 if mobile else 200
        logo = ft.Container(
            width=logo_width,
            height=logo_height,
            content=ft.Image(
                src="logo_bom.png.png",
                width=logo_width,
                height=logo_height,
                fit=ft.BoxFit.CONTAIN,
                border_radius=22,
            ),
            alignment=ft.Alignment(0, 0),
        )
        dashboard = GlassCard(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Smart Dashboard",
                                    size=18,
                                     color=theme.WHITE,
                                       weight=ft.FontWeight.W_800),
                            ft.Container(width=10,
                                          height=10,
                                            border_radius=99,
                                             bgcolor=theme.GREEN),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.Container(
    width=dashboard_inner_width,
    height=dashboard_inner_height,
    
    border_radius=ft.BorderRadius(
        top_left=1,
        top_right=1,
        bottom_left=1,
        bottom_right=1,
    ),
    gradient=theme.gradient(
        [   
            "#0950C2",    
        ],
        
    ),
    content=ft.Column(
        [
            ft.Icon(
                ft.Icons.SMART_TOY,
                size=48,
                color=theme.WHITE,
            ),
            ft.Text(
                "IA + RPA",
                size=28,
                weight=ft.FontWeight.W_800,
                color=theme.WHITE,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Operação em alta Performance",
                size=16,
                color=ft.Colors.with_opacity(0.84, theme.WHITE),
                text_align=ft.TextAlign.CENTER,
            ),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    ),
    alignment=ft.Alignment(0, 0),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            self.mini_stat("87%", "Menos Retrabalho",theme.GREEN),
                            self.mini_stat("24/7", "Execução Ativa", theme.GREEN),
                        ],
                        spacing=14,
                    ),
                    ft.Row(
                        [
                            self.progress_tile("Fluxos", 0.82, theme.BLUE),
                            self.progress_tile("Insights", 0.68, theme.BLUE),
                        ],
                        spacing=14,
                    ),
                ],
                spacing=16,
            ),
            padding=dashboard_padding,
        )

        hero_content = ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 12, "md": 6, "lg": 7},
                    width=10,
                    height=hero_text_height,
                    
                    content=ft.Column(
                        [
                            ft.Text(
                                "Transformando Empresas com Tecnologia Inteligente",
                                style=theme.title_style(hero_title_size),
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Text(
                                "Automação, IA, Sites e Aplicativos para acelerar o crescimento do seu negocio.",
                                color=theme.WHITE,
                                style=theme.body_style(hero_body_size),
                                text_align=ft.TextAlign.CENTER,
                            ),
                            ft.Container(
                                padding=ft.Padding(0, button_top_padding, 0, 0),
                                content=ft.Row(
                                [
                                    GlowButton("Solicitar Orçamento",
                                                ft.Icons.ROCKET_LAUNCH,
                                                  self.show_budget_form_handler()),
                                    
                                ],
                                wrap=False,
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER,
                                ),     
                            ),
                        ],
                        spacing=0,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(col={"xs": 12, "md": 6}, content=dashboard,
                              padding=ft.Padding(0, 0, 0, 0)),
            ],
            spacing=26,
            run_spacing=16 if mobile else 26,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            key="top",
            padding=ft.Padding(0, 18 if mobile else 34, 0, 32 if mobile else 56),
            content=max_width(
                ft.Column(
                    [
                        logo,
                        hero_content,
                    ],
                    spacing=14 if mobile else 0,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=18 if mobile else 56,
            ),
        )

    def mini_stat(self, value: str, label: str, color: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=10,
            border_radius=ft.BorderRadius(
                top_left=0,
                top_right=0,
                bottom_left=5,
                bottom_right=5,
            ),
            bgcolor=ft.Colors.with_opacity(0.10, theme.WHITE),
            content=ft.Column(
                [
                    ft.Text(value, size=26, weight=ft.FontWeight.W_800, color=color),
                    ft.Text(label, size=12, color=theme.WHITE),
                ],
                spacing=0,
            ),
        )

    def progress_tile(self, label: str,
                       value: float, color: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=16,
            border_radius=ft.BorderRadius(
                top_left=0,
                top_right=0,
                bottom_left=5,
                bottom_right=5,
            ),
            bgcolor=ft.Colors.with_opacity(
                0.08, theme.WHITE),
            content=ft.Column(
                [
                    ft.Text(label, color=theme.WHITE,
                             weight=ft.FontWeight.W_700),
                    ft.ProgressBar(value=value, color=color,
                                    bgcolor=ft.Colors.with_opacity(
                                        0.10, theme.WHITE)),
                ],
                spacing=10,
            ),
        )

    def services(self) -> ft.Control:
        cards = []
        for icon, title, desc in SERVICE_CARDS:
            cards.append(
                ft.Container(
                    col={"xs": 12, "sm": 6, "lg": 4},
                    content=GlassCard(
                        ft.Column(
                            [
                                ft.Icon(getattr(ft.Icons, icon.upper()), size=40, color="#0950C2"),
                                ft.Text(title, size=20,
                                         weight=ft.FontWeight.W_800,
                                           color=theme.WHITE),
                                ft.Text(desc, color=theme.WHITE,
                                         style=theme.body_style(14)),
                            ],
                            spacing=12,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=24,
                    ),
                )
            )
        return self.section(
            "dashboard",
            ft.Column(
                [
                    section_title("Dashboard Inteligente", 
                                   "Soluções digitais para acelerar sua empresa"
                                   ),
                    ft.ResponsiveRow(cards, 
                              spacing=18, 
                              run_spacing=18, 
                              alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=26,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def about(self) -> ft.Control:
        illustration = GlassCard(
            ft.Container(
                height=400,
                border_radius=ft.BorderRadius(
                    top_left=0,
                    top_right=0,
                    bottom_left=0,
                    bottom_right=0,
                ),
                gradient=ft.RadialGradient(
                    center=ft.Alignment(0, 0),
                    radius=0,
                    colors=[ft.Colors.with_opacity(0.5,
                                theme.BLUE),
                                ft.Colors.with_opacity(0.5,
                                theme.PURPLE),
                                "#0950C2"],
                ),
                content=ft.Stack(
                    [
                        ft.Container(),
                        ft.Container(
                            content=ft.Image(
                                src="logo.png.png",
                                width=460,
                                height=585,
                                fit=ft.BoxFit.COVER,
                                border_radius=32,
                            ),
                            alignment=ft.Alignment(0, 0),
                            expand=True,
                        ),
                        
                    ]
                ),
            ),
            padding=12,
        )
        content = ft.ResponsiveRow(
            [
                ft.Container(
                    col={"xs": 12, "md": 6},
                    content=ft.Column(
                        [
                            section_title("Sobre", "A SmartLoop pensa Tecnologia como Resultado"),
                            ft.Text(
                                "A SmartLoop Desenvolve Soluções Tecnologicas que Eliminam Tarefas Repetitivas, Reduzem Custos Operacionais e Aumentam a Produtividade Atraves da Automacao, Inteligencia Artificial e Desenvolvimento de Software sob Medida.",
                                color=theme.WHITE,
                                style=theme.body_style(17),
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                ),
                ft.Container(col={"xs": 12, "md": 6}, content=illustration),
            ],
            spacing=30,
            run_spacing=26,
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        return self.section("about", content)

    def portfolio(self) -> ft.Control:
        project_cards = [
            ft.Container(col={"xs": 12, "md": 4}, content=self.project_card(project))
            for project in PROJECTS
        ]
        return self.section(
            "portfolio",
            ft.Column(
                [
                    section_title("Portfólio de Projetos", "Soluções Digitais"),
                    ft.ResponsiveRow(project_cards, spacing=18,
                                      run_spacing=18,
                                        alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=26,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def project_card(self, project: dict) -> ft.Control:
        image = ft.Container(
            height=100,
            width=100,
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(2, 0, 0, 2),
            border_radius=ft.BorderRadius(
                    top_left=1,
                    top_right=1,
                    bottom_left=1,
                    bottom_right=1,
                ),
            gradient=theme.gradient([theme.BLUE, theme.BLUE, theme.BLUE]),
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ENGINEERING, size=48, color=theme.WHITE),
                    ft.Text(project["imagem"], size=24,
                             weight=ft.FontWeight.W_800, color=theme.WHITE),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
        )
        return GlassCard(
            ft.Column(
                [
                    image,
                    ft.Row(
                        [
                            ft.Text(project["categoria"],
                                     size=16, weight=ft.FontWeight.W_800, 
                                     color=theme.BLUE),
                            ft.Icon(ft.Icons.OPEN_IN_NEW,
                                     size=16,
                                     color=theme.MUTED),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Text(project["nome"], size=22, weight=ft.FontWeight.W_800,
                             color=theme.WHITE),
                    ft.Text(project["descricao"],
                             style=theme.body_style(16, theme.WHITE),
                             text_align=ft.TextAlign.CENTER,
                             width=260),
                    GlowButton("Acessar Projeto",
                                ft.Icons.ARROW_OUTWARD, 
                                self.project_link_handler(project),
                                  primary=False),
                ],
                spacing=14,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=18,
        )

    def project_link_handler(self, project: dict):
        async def handler(_):
            if str(project.get("link", "")).startswith("demo:"):
                self.show_project_demo(project)
                return

            await self.open_url(project["link"])

        return handler

    def demo_stat(self, value: str, label: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=14,
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.10, theme.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.14, theme.WHITE)),
            content=ft.Column(
                [
                    ft.Text(value, size=24, weight=ft.FontWeight.W_800, color=theme.GREEN),
                    ft.Text(label, size=12, color=theme.WHITE, text_align=ft.TextAlign.CENTER),
                ],
                spacing=2,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def demo_list_card(self, title: str, items: list[str], icon: str) -> ft.Control:
        return ft.Container(
            expand=True,
            padding=18,
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.08, theme.WHITE),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.14, theme.WHITE)),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(icon, size=20, color=theme.GREEN),
                            ft.Text(title, size=17, weight=ft.FontWeight.W_800, color=theme.WHITE),
                        ],
                        spacing=8,
                    ),
                    *[
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.CHECK_CIRCLE, size=16, color=theme.GREEN),
                                ft.Text(item, size=13, color=theme.WHITE, expand=True),
                            ],
                            spacing=8,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        )
                        for item in items
                    ],
                ],
                spacing=10,
            ),
        )

    def demo_mockup(self, project: dict) -> ft.Control:
        return ft.Container(
            height=300,
            padding=18,
            border_radius=8,
            gradient=theme.gradient(["#07111F", "#0950C2", "#111827"]),
            border=ft.Border.all(1, ft.Colors.with_opacity(0.16, theme.WHITE)),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(project["imagem"], size=28, weight=ft.FontWeight.W_800, color=theme.WHITE),
                            ft.Container(width=10, height=10, border_radius=99, bgcolor=theme.GREEN),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        expand=True,
                        border_radius=8,
                        bgcolor=ft.Colors.with_opacity(0.14, theme.WHITE),
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE, size=58, color=theme.WHITE),
                                ft.Text(project["demo_titulo"], size=18, weight=ft.FontWeight.W_800, color=theme.WHITE, text_align=ft.TextAlign.CENTER),
                                ft.Text("Demo conceitual SmartLoop", size=13, color=ft.Colors.with_opacity(0.82, theme.WHITE)),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=8,
                        ),
                    ),
                ],
                spacing=14,
            ),
        )

    def show_project_demo(self, project: dict):
        def close_demo(_=None):
            if demo_overlay in self.page.overlay:
                self.page.overlay.remove(demo_overlay)
            self.page.update()

        metrics = project.get("demo_metricas", [])
        feature_items = project.get("demo_funcionalidades", [])
        benefit_items = project.get("demo_beneficios", [])

        demo_overlay = ft.Container(
            width=900,
            height=800,
            bgcolor=ft.Colors.with_opacity(0.88, "#020617"),
            alignment=ft.Alignment(0, 0),
            padding=18,
            content=ft.Container(
                width=980,
                padding=20,
                border_radius=14,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(project["nome"], size=28, weight=ft.FontWeight.W_800, color=theme.WHITE),
                                        ft.Text(project["categoria"], size=14, color=theme.GREEN, weight=ft.FontWeight.W_700),
                                    ],
                                    spacing=2,
                                ),
                                ft.TextButton("Voltar", icon=ft.Icons.ARROW_BACK, on_click=close_demo, style=ft.ButtonStyle(color=theme.GREEN)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Container(
                                    col={"xs": 12, "md": 6},
                                    content=ft.Column(
                                        [
                                            ft.Text(project["demo_titulo"], style=theme.title_style(34)),
                                            ft.Text(project["demo_resumo"], style=theme.body_style(16, theme.WHITE)),
                                            ft.Row(
                                                [self.demo_stat(value, label) for value, label in metrics],
                                                spacing=10,
                                            ),
                                            GlowButton(
                                                "Solicitar projeto parecido",
                                                ft.Icons.ROCKET_LAUNCH,
                                                self.show_budget_form_handler(),
                                            ),
                                        ],
                                        spacing=16,
                                    ),
                                ),
                                ft.Container(col={"xs": 12, "md": 6}, content=self.demo_mockup(project)),
                            ],
                            spacing=18,
                            run_spacing=18,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Container(
                                    col={"xs": 12, "md": 6},
                                    content=self.demo_list_card("Funcionalidades", feature_items, ft.Icons.AUTO_AWESOME),
                                ),
                                ft.Container(
                                    col={"xs": 12, "md": 6},
                                    content=self.demo_list_card("Beneficios", benefit_items, ft.Icons.TRENDING_UP),
                                ),
                            ],
                            spacing=14,
                            run_spacing=14,
                        ),
                    ],
                    spacing=18,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )
        self.page.overlay.append(demo_overlay)
        self.page.update()

    def agent_bubble(self, role: str, text: str) -> ft.Control:
        is_user = role == "user"
        page_width = self.page.width or 390
        compact_agent = page_width < 1200
        panel_width = 300 if compact_agent else 520
        bubble_width = panel_width - 56
        wrapped_text = "\n".join(textwrap.wrap(text, width=32 if compact_agent else 54))
        return ft.Container(
            width=panel_width - 20,
            alignment=ft.Alignment(1, 0) if is_user else ft.Alignment(-1, 0),
            content=ft.Container(
                    width=bubble_width,
                    padding=12,
                    border_radius=8,
                    bgcolor=theme.GREEN if is_user else ft.Colors.with_opacity(0.10, theme.WHITE),
                    border=None if is_user else ft.Border.all(1, ft.Colors.with_opacity(0.16, theme.WHITE)),
                    content=ft.Text(
                        wrapped_text,
                        width=bubble_width - 24,
                        color=theme.WHITE,
                        size=13 if compact_agent else 14,
                        no_wrap=False,
                        max_lines=10,
                        overflow=ft.TextOverflow.VISIBLE,
                    ),
                ),
        )

    def refresh_agent_messages(self):
        self.agent_messages_column.controls = [
            self.agent_bubble(role, message)
            for role, message in self.agent_messages
        ]

    def show_ai_agent(self):
        page_width = self.page.width or 390
        page_height = self.page.height or 780
        compact_agent = page_width < 1200
        panel_width = 300 if compact_agent else 520
        panel_height = min(560, page_height - 120) if compact_agent else 620
        self.refresh_agent_messages()

        async def send_message(_=None):
            question = (self.agent_input.value or "").strip()
            if not question:
                return

            self.agent_messages.append(("user", question))
            self.agent_messages.append(("agent", "Pensando..."))
            self.agent_input.value = ""
            self.refresh_agent_messages()
            self.page.update()

            answer = await asyncio.to_thread(ask_smartloop_ai, question)
            self.agent_messages[-1] = ("agent", answer)
            self.refresh_agent_messages()
            self.page.update()

        def close_agent(_=None):
            if agent_overlay in self.page.overlay:
                self.page.overlay.remove(agent_overlay)
            self.page.update()

        agent_overlay = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.72, "#020617"),
            alignment=ft.Alignment(0, 0) if compact_agent else ft.Alignment(1, 1),
            padding=8 if compact_agent else 22,
            content=ft.Container(
                width=panel_width,
                height=panel_height,
                padding=10 if compact_agent else 18,
                border_radius=14,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SMART_TOY, color=theme.GREEN, size=24),
                                ft.Text(
                                    "Agente SmartLoop",
                                    color=theme.WHITE,
                                    size=18 if compact_agent else 22,
                                    weight=ft.FontWeight.W_800,
                                    expand=True,
                                ),
                                ft.IconButton(ft.Icons.CLOSE, icon_color=theme.WHITE, on_click=close_agent),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Container(
                            expand=True,
                            padding=8 if compact_agent else 12,
                            border_radius=8,
                            bgcolor=ft.Colors.with_opacity(0.06, theme.WHITE),
                            content=self.agent_messages_column,
                        ),
                        ft.Row(
                            [
                                ft.Container(expand=True, content=self.agent_input),
                                ft.IconButton(
                                    ft.Icons.SEND,
                                    icon_color=theme.WHITE,
                                    bgcolor=theme.GREEN,
                                    on_click=send_message,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.END,
                        ),
                        ft.Text(
                            "Respostas geradas por IA. Para proposta comercial, solicite um orcamento.",
                            size=11,
                            color=ft.Colors.with_opacity(0.70, theme.WHITE),
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=12,
                ),
            ),
        )
        self.page.overlay.append(agent_overlay)
        self.page.update()

    def metrics(self) -> ft.Control:
        cards = []
        self.metric_values = []
        for label, _, prefix, suffix in METRICS:
            value = ft.Text(f"{prefix}0{suffix}", size=34,
                             weight=ft.FontWeight.W_800,
                               color=theme.WHITE)
            self.metric_values.append(value)
            cards.append(
                ft.Container(
                    col={"xs": 12, "sm": 6, "lg": 3},
                    content=GlassCard(
                        ft.Column(
                            [
                                value,
                                ft.Text(label, color=theme.WHITE, size=16),
                            ],
                            spacing=6,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=26,
                    ),
                )
            )
        return self.section("metrics", 
                            ft.ResponsiveRow(cards, spacing=18,
                                              run_spacing=18,
                                                alignment=ft.MainAxisAlignment.CENTER))

    def differentials(self) -> ft.Control:
        cards = []
        for icon, title in DIFFERENTIALS:
            cards.append(
                ft.Container(
                    col={"xs": 12, "sm": 6, "lg": 4},
                    content=GlassCard(
                        ft.Row(
                            [
                                ft.Icon(getattr(ft.Icons,
                                                 icon.upper()), 
                                                 size=28, color=theme.GREEN),
                                ft.Text(title, size=14,
                                         weight=ft.FontWeight.W_800,
                                           color=theme.WHITE),
                            ],
                            spacing=14,
                             alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=22,
                    ),
                )
            )
        return self.section(
            "differentials",
            ft.Column(
                [
                    section_title("Diferenciais", "Tecnologia com Velocidade, Segurança e Critério"),
                    ft.ResponsiveRow(cards, spacing=18, run_spacing=18, alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=26,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def testimonials(self) -> ft.Control:
        self.testimonial_box.content = self.testimonial_card(TESTIMONIALS[0])
        return self.section(
            "testimonials",
            ft.Column(
                [
                    section_title("Depoimentos", "Clientes que ganharam tempo para crescer"),
                    ft.Container(width=720, content=self.testimonial_box),
                ],
                spacing=26,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def testimonial_card(self, item: dict) -> ft.Control:
        return GlassCard(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.CircleAvatar(
                                content=ft.Text(item["iniciais"],
                                                 color=theme.WHITE,
                                                   weight=ft.FontWeight.W_800),
                                bgcolor=theme.BLUE,
                                radius=32,
                            ),
                            ft.Column(
                                [
                                    ft.Text(item["nome"], size=18,
                                             weight=ft.FontWeight.W_800,
                                               color=theme.WHITE),
                                    ft.Text(item["cargo"], size=13,
                                             color=theme.CYAN),
                                ],
                                spacing=2,
                                 
                            ),
                        ],
                        spacing=14,
                         alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Text(f'"{item["texto"]}"',
                             style=theme.body_style(18,
                                                     theme.WHITE)),
                ],
                spacing=18,
            ),
            padding=26,
        )

    def final_cta(self) -> ft.Control:
        mobile = self.is_mobile()
        return self.section(
            "cta",
            GlassCard(
                ft.Column(
                    [
                        ft.Text("Pronto para Automatizar seu Negocio?", style=theme.title_style(29 if mobile else 42), text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            "Vamos Desenhar um Fluxo mais Rápido, Inteligente e Lucrativo para sua Empresa.",
                            color=theme.WHITE,
                            style=theme.body_style(15 if mobile else 17),
                            text_align=ft.TextAlign.CENTER,
                            width=300 if mobile else None,
                        ),
                        GlowButton("Falar no WhatsApp",
                                    ft.Icons.CHAT_BUBBLE,
                                      url=CONTACT.whatsapp),
                    ],
                    spacing=14 if mobile else 18,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=22 if mobile else 36,
                gradient_colors=[ft.Colors.with_opacity(0.25, theme.BLUE),
                                 ft.Colors.with_opacity(0.10, theme.PURPLE)
                                 ],
            ),
        )

    def footer(self) -> ft.Control:
        mobile = self.is_mobile()
        links = [
            ("Email", f"mailto:{CONTACT.email}"),
            ("WhatsApp", CONTACT.whatsapp),
            ("Instagram", CONTACT.instagram),
            ("LinkedIn", CONTACT.linkedin),
            ("GitHub", CONTACT.github),
        ]
        return ft.Container(
            padding=ft.Padding(0, 20 if mobile else 28, 0, 26 if mobile else 34),
            content=max_width(
                ft.Column(
                    [
                        ft.Text("SmartLoop", size=26, weight=ft.FontWeight.W_800,
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text("Automação • IA • Sites • Aplicativos",
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER,
                                 width=310 if mobile else None),
                        ft.Text("© 2024 SmartLoop. Todos os direitos reservados",
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER,
                                 width=310 if mobile else None),
                        ft.Text(
                            "Desenvolvido por SmartLoop. Valter Lira. Tecnologia Python",
                            color=theme.WHITE,
                            text_align=ft.TextAlign.CENTER,
                            width=310 if mobile else None,
                        ),         
                        ft.Container(
                            width=330 if mobile else 720,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Markdown(
                                "  |  ".join([f"[{label}]({url})" for label, url in links]),
                                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                                auto_follow_links=True,
                                auto_follow_links_target=ft.UrlTarget.BLANK,
                                selectable=False,
                                shrink_wrap=True,
                            ),
                        ),
                    ],
                    spacing=7 if mobile else 8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=18 if mobile else 56,
            ),
        )

    def section(self, key: str, content: ft.Control) -> ft.Control:
        mobile = self.is_mobile()
        return ft.Container(
            key=key,
            padding=ft.Padding(0, 28 if mobile else 46, 0, 28 if mobile else 46),
            content=max_width(content, padding=18 if mobile else 56),
        )

    def show_budget_form_handler(self):
        async def handler(_):
            self.show_budget_form()

        return handler

    def form_field(self, label: str, multiline: bool = False) -> ft.Container:
        field = ft.TextField(
            label=label,
            multiline=multiline,
            min_lines=3 if multiline else None,
            max_lines=5 if multiline else None,
            color=theme.WHITE,
            border=ft.InputBorder.NONE,
            label_style=ft.TextStyle(color=theme.WHITE),
            content_padding=ft.Padding(14, 10, 14, 10),
        )
        return self.form_input_box(field)

    def form_input_box(self, field) -> ft.Container:
        default_border = ft.Colors.with_opacity(0.35, theme.WHITE)

        box = ft.Container(
            border=ft.Border.all(1, default_border),
            border_radius=8,
            animate=ft.Animation(180, ft.AnimationCurve.EASE_OUT),
        )
        box.data = field

        def set_active(active: bool):
            box.border = ft.Border.all(1.8 if active else 1, theme.GREEN if active else default_border)
            box.update()

        def enter(_):
            set_active(True)

        def exit(_):
            set_active(False)

        field.on_focus = enter
        field.on_blur = exit
        box.content = ft.GestureDetector(
            content=field,
            on_enter=enter,
            on_exit=exit,
        )
        return box

    def formulario_antigo_alerta(self):
        nome = self.form_field("Seu nome")
        empresa = self.form_field("Nome da empresa")
        whatsapp = self.form_field("WhatsApp")
        email = self.form_field("Email")
        segmento = self.form_field("Segmento do negocio")
        objetivo = self.form_field("Qual problema voce quer resolver?", multiline=True)
        detalhes = self.form_field("Conte mais detalhes do projeto", multiline=True)
        tipo_projeto = ft.Dropdown(
            label="Qual projeto de tecnologia voce quer fazer?",
            value="Ainda nao sei",
            options=[
                ft.DropdownOption("Automação RPA"),
                ft.DropdownOption("Site ou Landing Page"),
                ft.DropdownOption("Aplicativo Mobile/Web"),
                ft.DropdownOption("Inteligência Artificial"),
                ft.DropdownOption("Integração de Sistemas"),
                ft.DropdownOption("Ainda nao sei"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        prazo = ft.Dropdown(
            label="Prazo desejado",
            options=[
                ft.DropdownOption("Urgente"),
                ft.DropdownOption("15 a 30 dias"),
                ft.DropdownOption("1 a 3 meses"),
                ft.DropdownOption("Sem prazo definido"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        orcamento = ft.Dropdown(
            label="Faixa de investimento",
            options=[
                ft.DropdownOption("Ate R$ 3.000"),
                ft.DropdownOption("R$ 3.000 a R$ 10.000"),
                ft.DropdownOption("R$ 10.000 a R$ 30.000"),
                ft.DropdownOption("Acima de R$ 30.000"),
                ft.DropdownOption("Quero orientação"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        status = ft.Text("", color=theme.GREEN, size=13)

        async def close_dialog(_=None):
            dialog.open = False
            self.page.pop_dialog()
            self.page.update()
            await self.page.scroll_to(
                offset=0,
                duration=500,
                curve=ft.AnimationCurve.EASE_IN_OUT,
            )

        dialog = ft.AlertDialog(
            modal=True,
            bgcolor="#0F172A",
            title=ft.Text("Solicitar Orçamento", color=theme.WHITE, weight=ft.FontWeight.W_800),
            content=ft.Container(
                width=720,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Voltar para página",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=close_dialog,
                                    style=ft.ButtonStyle(color=theme.GREEN),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                        ft.Text(
                            "Preencha as informações para a SmartLoop entender seu negocio e entrar em contato.",
                            color=theme.WHITE,
                            size=14,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Container(col={"xs": 12, "md": 6}, content=nome),
                                ft.Container(col={"xs": 12, "md": 6}, content=empresa),
                                ft.Container(col={"xs": 12, "md": 6}, content=whatsapp),
                                ft.Container(col={"xs": 12, "md": 6}, content=email),
                                ft.Container(col={"xs": 12, "md": 6}, content=segmento),
                                ft.Container(col={"xs": 12, "md": 6}, content=tipo_projeto),
                                ft.Container(col={"xs": 12, "md": 6}, content=prazo),
                                ft.Container(col={"xs": 12, "md": 6}, content=orcamento),
                                ft.Container(col=12, content=objetivo),
                                ft.Container(col=12, content=detalhes),
                            ],
                            spacing=12,
                            run_spacing=12,
                        ),
                        status,
                    ],
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions_alignment=ft.MainAxisAlignment.END,
        )

        async def submit_form(_):
            print("Clique recebido no botao Salvar lead")
            required = [
                (nome, "Informe seu nome."),
                (empresa, "Informe o nome da empresa."),
                (whatsapp, "Informe seu WhatsApp."),
                (objetivo, "Explique o objetivo do projeto."),
            ]
            for field, message in required:
                if not field.value.strip():
                    print(f"Lead nao salvo: {message}")
                    status.value = message
                    status.color = "#FCA5A5"
                    self.page.update()
                    return

            if not tipo_projeto.value:
                print("Lead nao salvo: escolha o tipo de projeto.")
                status.value = "Escolha o tipo de projeto."
                status.color = "#FCA5A5"
                self.page.update()
                return

            lead_id = save_lead(
                {
                    "nome": nome.value,
                    "empresa": empresa.value,
                    "whatsapp": whatsapp.value,
                    "email": email.value,
                    "segmento": segmento.value,
                    "tipo_projeto": tipo_projeto.value,
                    "objetivo": objetivo.value,
                    "prazo": prazo.value or "",
                    "orcamento": orcamento.value or "",
                    "detalhes": detalhes.value,
                }
            )
            await close_dialog()

        dialog.actions = [
            ft.TextButton("Cancelar e voltar", icon=ft.Icons.ARROW_BACK, on_click=close_dialog, style=ft.ButtonStyle(color=theme.WHITE)),
            ft.Button("Salvar lead", icon=ft.Icons.SAVE, bgcolor=theme.GREEN, color=theme.WHITE, on_click=submit_form),
        ]
        self.page.show_dialog(dialog)
        self.page.update()

    def formulario_antigo_overlay(self):
        nome = self.form_field("Seu nome")
        empresa = self.form_field("Nome da empresa")
        whatsapp = self.form_field("WhatsApp")
        email = self.form_field("Email")
        segmento = self.form_field("Segmento do negocio")
        objetivo = self.form_field("Qual problema voce quer resolver?", multiline=True)
        detalhes = self.form_field("Conte mais detalhes do projeto", multiline=True)
        tipo_projeto = ft.Dropdown(
            label="Qual projeto de tecnologia voce quer fazer?",
            options=[
                ft.DropdownOption("Automação RPA"),
                ft.DropdownOption("Site ou Landing Page"),
                ft.DropdownOption("Aplicativo Mobile/Web"),
                ft.DropdownOption("Inteligência Artificial"),
                ft.DropdownOption("Integração de Sistemas"),
                ft.DropdownOption("Ainda não sei"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        prazo = ft.Dropdown(
            label="Prazo desejado",
            options=[
                ft.DropdownOption("Urgente"),
                ft.DropdownOption("15 a 30 dias"),
                ft.DropdownOption("1 a 3 meses"),
                ft.DropdownOption("Sem prazo definido"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        orcamento = ft.Dropdown(
            label="Faixa de investimento",
            options=[
                ft.DropdownOption("Ate R$ 3.000"),
                ft.DropdownOption("R$ 3.000 a R$ 10.000"),
                ft.DropdownOption("R$ 10.000 a R$ 30.000"),
                ft.DropdownOption("Acima de R$ 30.000"),
                ft.DropdownOption("Quero orientação"),
            ],
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            border_radius=8,
        )
        status = ft.Text("", color=theme.GREEN, size=13)

        def close_form(_=None):
            if form_overlay in self.page.overlay:
                self.page.overlay.remove(form_overlay)
            self.page.update()

        def submit_form(_):
            print("Clique recebido no botao Salvar lead")
            try:
                def value(control):
                    return (control.value or "").strip()

                required = [
                    (nome, "Informe seu nome."),
                    (empresa, "Informe o nome da empresa."),
                    (whatsapp, "Informe seu WhatsApp."),
                ]
                for field, message in required:
                    if not value(field):
                        print(f"Lead nao salvo: {message}")
                        status.value = message
                        status.color = "#FCA5A5"
                        self.page.update()
                        return

                lead_id = save_lead(
                    {
                        "nome": value(nome),
                        "empresa": value(empresa),
                        "whatsapp": value(whatsapp),
                        "email": value(email),
                        "segmento": value(segmento),
                        "tipo_projeto": value(tipo_projeto) or "Ainda nao sei",
                        "objetivo": value(objetivo) or "Nao informado",
                        "prazo": value(prazo),
                        "orcamento": value(orcamento),
                        "detalhes": value(detalhes),
                    }
                )
                print(f"Lead salvo no banco leads.db com codigo #{lead_id}")
                close_form()
            except Exception as error:
                print(f"Erro ao salvar lead: {error}")
                status.value = f"Erro ao salvar: {error}"
                status.color = "#FCA5A5"
                self.page.update()

        form_overlay = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.82, "#020617"),
            alignment=ft.Alignment(0, 0),
            padding=24,
            content=ft.Container(
                width=780,
                height=680,
                padding=24,
                border_radius=18,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Solicitar Orçamento", color=theme.WHITE, size=24, weight=ft.FontWeight.W_800),
                                ft.TextButton(
                                    "Voltar para pagina",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=close_form,
                                    style=ft.ButtonStyle(color=theme.GREEN),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            "Preencha as informações para a SmartLoop entender seu negocio e entrar em contato.",
                            color=theme.WHITE,
                            size=14,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Container(col={"xs": 12, "md": 6}, content=nome),
                                ft.Container(col={"xs": 12, "md": 6}, content=empresa),
                                ft.Container(col={"xs": 12, "md": 6}, content=whatsapp),
                                ft.Container(col={"xs": 12, "md": 6}, content=email),
                                ft.Container(col={"xs": 12, "md": 6}, content=segmento),
                                ft.Container(col={"xs": 12, "md": 6}, content=tipo_projeto),
                                ft.Container(col={"xs": 12, "md": 6}, content=prazo),
                                ft.Container(col={"xs": 12, "md": 6}, content=orcamento),
                                ft.Container(col=12, content=objetivo),
                                ft.Container(col=12, content=detalhes),
                            ],
                            spacing=12,
                            run_spacing=12,
                        ),
                        status,
                        ft.Row(
                            [
                                ft.TextButton(
                                    "Cancelar e voltar",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=close_form,
                                    style=ft.ButtonStyle(color=theme.WHITE),
                                ),
                                ft.Button(
                                    "Salvar lead",
                                    icon=ft.Icons.SAVE,
                                    on_click=submit_form,
                                    bgcolor=theme.GREEN,
                                    color=theme.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )
        self.page.overlay.append(form_overlay)
        self.page.update()

    async def open_url(self, url: str):
        result = self.page.launch_url(url)
        if inspect.isawaitable(result):
            await result

    async def scroll_to(self, key: str):
        await self.page.scroll_to(scroll_key=key,
                                   duration=700, 
                                   curve=ft.AnimationCurve.EASE_IN_OUT)

    def open_url_handler(self, url: str):
        async def handler(_):
            await self.open_url(url)

        return handler

    def scroll_handler(self, key: str):
        async def handler(_):
            await self.scroll_to(key)

        return handler

    def show_budget_form(self):
        nome = self.form_field("Seu nome")
        empresa = self.form_field("Nome da empresa")
        whatsapp = self.form_field("WhatsApp")
        email = self.form_field("Email")
        segmento = self.form_field("Segmento da empresa")
        tipo_projeto = self.form_input_box(
            ft.Dropdown(
                label="Projeto desejado",
                value="Ainda nao sei",
                options=[
                    ft.DropdownOption("Automação RPA"),
                    ft.DropdownOption("Site ou Landing Page"),
                    ft.DropdownOption("Aplicativo Mobile/Web"),
                    ft.DropdownOption("Inteligência Artificial"),
                    ft.DropdownOption("Integração de Sistemas"),
                    ft.DropdownOption("Ainda nao sei"),
                ],
                color=theme.WHITE,
                border=ft.InputBorder.NONE,
                label_style=ft.TextStyle(color=theme.WHITE),
                content_padding=ft.Padding(14, 10, 14, 10),
            )
        )
        prazo = self.form_input_box(
            ft.Dropdown(
                label="Prazo desejado",
                value="Sem prazo definido",
                options=[
                    ft.DropdownOption("Urgente"),
                    ft.DropdownOption("15 a 30 dias"),
                    ft.DropdownOption("1 a 3 meses"),
                    ft.DropdownOption("Sem prazo definido"),
                ],
                color=theme.WHITE,
                border=ft.InputBorder.NONE,
                label_style=ft.TextStyle(color=theme.WHITE),
                content_padding=ft.Padding(14, 10, 14, 10),
            )
        )
        orcamento = self.form_input_box(
            ft.Dropdown(
                label="Orçamento Aproximado",
                value="Quero Orientação",
                options=[
                    ft.DropdownOption("Ate R$ 3.000"),
                    ft.DropdownOption("R$ 3.000 a R$ 10.000"),
                    ft.DropdownOption("R$ 10.000 a R$ 30.000"),
                    ft.DropdownOption("Acima de R$ 30.000"),
                    ft.DropdownOption("Quero Orientação"),
                ],
                color=theme.WHITE,
                border=ft.InputBorder.NONE,
                label_style=ft.TextStyle(color=theme.WHITE),
                content_padding=ft.Padding(14, 10, 14, 10),
            )
        )
        objetivo = self.form_field("Conte o que voce precisa", multiline=True)
        detalhes = self.form_field("Detalhes adicionais", multiline=True)
        objetivo.data.min_lines = 2
        objetivo.data.max_lines = 3
        detalhes.data.min_lines = 2
        detalhes.data.max_lines = 3
        status = ft.Text("", color=theme.GREEN, size=13)

        def safe_value(control):
            field = control.data if isinstance(control, ft.Container) and control.data else control
            return (field.value or "").strip()

        def close_form(_=None):
            if form_overlay in self.page.overlay:
                self.page.overlay.remove(form_overlay)
            self.page.update()

        def submit_form(_):
            print("Clique recebido no botao Salvar lead")
            status.value = "Salvando lead..."
            status.color = theme.GREEN
            self.page.update()
            try:
                lead_id = save_lead(
                    {
                        "nome": safe_value(nome) or "Nao informado",
                        "empresa": safe_value(empresa) or "Nao informado",
                        "whatsapp": safe_value(whatsapp) or "Nao informado",
                        "email": safe_value(email),
                        "segmento": safe_value(segmento),
                        "tipo_projeto": safe_value(tipo_projeto) or "Nao informado",
                        "objetivo": safe_value(objetivo) or "Nao informado",
                        "prazo": safe_value(prazo),
                        "orcamento": safe_value(orcamento),
                        "detalhes": safe_value(detalhes),
                    }
                )
                print(f"Lead salvo no banco leads.db com codigo #{lead_id}")
                close_form()
            except Exception as error:
                print(f"Erro ao salvar lead: {error}")
                status.value = f"Erro ao salvar: {error}"
                status.color = "#FCA5A5"
                self.page.update()

        form_overlay = ft.Container(
            width=800,
            height=600,
            bgcolor=ft.Colors.with_opacity(0.86, "#020617"),
            alignment=ft.Alignment(0, 0),
            padding=16,
            content=ft.Container(
                width=620,
                padding=16,
                border_radius=14,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("Solicitar Orcamento", color=theme.WHITE, size=21, weight=ft.FontWeight.W_800),
                                ft.TextButton("Voltar", icon=ft.Icons.ARROW_BACK, on_click=close_form, style=ft.ButtonStyle(color=theme.GREEN)),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Container(col={"xs": 12, "md": 6}, content=nome),
                                ft.Container(col={"xs": 12, "md": 6}, content=empresa),
                                ft.Container(col={"xs": 12, "md": 6}, content=whatsapp),
                                ft.Container(col={"xs": 12, "md": 6}, content=email),
                                ft.Container(col={"xs": 12, "md": 6}, content=segmento),
                                ft.Container(col={"xs": 12, "md": 6}, content=tipo_projeto),
                                ft.Container(col={"xs": 12, "md": 6}, content=prazo),
                                ft.Container(col={"xs": 12, "md": 6}, content=orcamento),
                                ft.Container(col={"xs": 12, "md": 6}, content=objetivo),
                                ft.Container(col={"xs": 12, "md": 6}, content=detalhes),
                            ],
                            spacing=9,
                            run_spacing=9,
                        ),
                        status,
                        ft.Row(
                            [
                                ft.TextButton("Cancelar", on_click=close_form, style=ft.ButtonStyle(color=theme.WHITE)),
                                ft.TextButton("Salvar lead", icon=ft.Icons.SAVE, on_click=submit_form, style=ft.ButtonStyle(color=theme.GREEN)),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=9,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )
        self.page.overlay.append(form_overlay)
        self.page.update()

    def start_animations(self):
        threading.Thread(target=self._animate_metrics, daemon=True).start()
        threading.Thread(target=self._rotate_testimonials, daemon=True).start()

    def _animate_metrics(self):
        time.sleep(0.65)
        for step in range(1, 41):
            for idx, (_, target, prefix, suffix) in enumerate(METRICS):
                current = round(target * step / 40)
                self.metric_values[idx].value = f"{prefix}{current}{suffix}"
            self.page.update()
            time.sleep(0.035)

    def _rotate_testimonials(self):
        while True:
            time.sleep(4.2)
            self.testimonial_index = (self.testimonial_index + 1) % len(TESTIMONIALS)
            self.testimonial_box.content = self.testimonial_card(TESTIMONIALS[self.testimonial_index])
            self.page.update()
