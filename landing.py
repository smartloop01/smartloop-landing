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
from ai_agent_service import ask_smartluup_ai
from lead_service import init_db, save_lead


# Cards exibidos na secao "Dashboard Inteligente".
SERVICE_CARDS = [
    ("smart_toy", "Automação RPA", "Robos que executam processos repetitivos com precisão."),
    ("language", "Desenvolvimento Web", "Sites, portais e sistemas rapidos para vender e operar melhor."),
    ("phone_iphone", "Aplicativos Mobile", "Apps mobile e web com experiencia fluida e escalavel."),
    ("psychology", "Inteligência Artificial", "IA aplicada para decisões, atendimento e produtividade."),
    ("analytics", "Integraçâo de Sistemas", "Dados conectados entre plataformas, equipes e indicadores."),
    ("cloud_queue", "Soluções em Nuvem", "Arquiteturas seguras para crescer sem travar a operação."),
]

# Cards exibidos na secao "Diferenciais".
DIFFERENTIALS = [
    ("bolt", "Entrega Rápida"),
    ("smart_toy", "Especialistas em IA"),
    ("sync", "Automação Inteligente"),
    ("trending_up", "Escalabilidade"),
    ("shield", "Segurança"),
    ("ads_click", "Soluções Sob Medida"),
]

# Numeros animados exibidos na secao de metricas da empresa.
METRICS = [
    ("Projetos", 23, "+", ""),
    ("Mil horas automatizadas", 100, "+", " mil"),
    ("Clientes", 23, "+", ""),
    ("Satisfação", 98, "", "%"),
]


# Textos exibidos quando o visitante clica nas politicas do rodape.
PRIVACY_POLICIES = {
    "Politica de Privacidade": [
        "A SmartLuup respeita a sua privacidade e está comprometida com a proteção dos dados pessoais de seus usuários, clientes e visitantes. Esta Política de Privacidade explica como coletamos, utilizamos, armazenamos e protegemos suas informações.\n\n"

"1."" Coleta de Informações\n\n"

"Podemos coletar as seguintes informações:\n\n"

"Nome completo;"
"E-mail;"
"Telefone;"
"Nome da empresa;"
"Cargo ou função;"
"Informações fornecidas por formulários de contato;"
"Dados de navegação, endereço IP, cookies e informações do dispositivo.\n\n"
"2." "Uso das Informações\n\n"

"As informações coletadas poderão ser utilizadas para:\n\n"

"Prestar nossos serviços;"
"Entrar em contato com clientes e interessados;"
"Enviar propostas comerciais;"
"Melhorar a experiência do usuário;"
"Personalizar conteúdos e funcionalidades;"
"Cumprir obrigações legais e regulatórias;"
"Garantir a segurança dos sistemas e serviços.\n\n"
"3." "Compartilhamento de Dados\n\n"

"A SmartLuup não vende informações pessoais. Os dados poderão ser compartilhados apenas com:\n\n"

"Prestadores de serviços necessários para a operação da plataforma;"
"Autoridades governamentais quando exigido por lei;"
"Parceiros tecnológicos responsáveis pela hospedagem, processamento e segurança dos dados.\n\n"
"4." "Armazenamento e Segurança\n\n"

"Adotamos medidas técnicas e organizacionais para proteger os dados contra acesso não autorizado, perda, alteração ou divulgação indevida.\n\n"

"Os dados são armazenados em ambientes seguros e monitorados, utilizando tecnologias modernas de proteção da informação.\n\n"

"5." "Cookies\n\n"

"Utilizamos cookies para melhorar a navegação, analisar o tráfego do site e oferecer uma experiência personalizada.\n\n"

"O usuário pode desabilitar os cookies nas configurações do navegador, ciente de que algumas funcionalidades poderão ser afetadas.\n\n"

"6." "Direitos do Titular dos Dados\n\n"

"Nos termos da Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018), o usuário poderá solicitar:\n\n"

"Confirmação da existência de tratamento de dados;"
"Acesso aos dados pessoais;"
"Correção de dados incompletos ou incorretos;"
"Exclusão dos dados quando aplicável;"
"Portabilidade dos dados;"
"Revogação do consentimento.\n\n"
"7." "Retenção dos Dados\n\n"

"Os dados serão mantidos pelo período necessário para cumprir as finalidades descritas nesta Política ou conforme exigido por lei.\n\n"

"8." "Alterações desta Política\n\n"

"Esta Política de Privacidade poderá ser atualizada periodicamente. As alterações entrarão em vigor após sua publicação em nosso site.\n\n"

"9." "Contato\n\n"

"Em caso de dúvidas sobre esta Política de Privacidade ou sobre o tratamento de dados pessoais, entre em contato:\n\n"

"SmartLuup Tecnologia\n"
"E-mail: contato@smartluup.com.br\n"
"Site: www.smartluup.com.br\n\n"

"Ao utilizar nossos serviços, você concorda com os termos desta Política de Privacidade.",
    ],
    "Termos de Uso": [
        "Última atualização: 20 de julho de 2026\n\n"

        "Bem-vindo à SmartLuup.\n Ao acessar ou utilizar nossos serviços, você concorda com os presentes Termos de Uso.\n\n"

        "1. Objetivo\n\n"

"A SmartLuup oferece soluções de tecnologia, automação de processos (RPA), desenvolvimento de sistemas, aplicativos, websites, inteligência artificial, CRM e outras soluções corporativas.\n\n"

"2. Cadastro\n\n"

"Ao fornecer informações em formulários ou plataformas da SmartLuup, o usuário declara que os dados informados são verdadeiros e atualizados.\n\n"

"3. Uso Permitido\n\n"

"O usuário compromete-se a utilizar os serviços de forma lícita, ética e em conformidade com a legislação vigente.\n\n"

"É proibido:\n\n"

"Utilizar os serviços para atividades ilegais;\n"
"Tentar acessar sistemas sem autorização;\n"
"Distribuir códigos maliciosos;\n"
"Violar direitos de terceiros.\n\n"
"4. Propriedade Intelectual\n\n"

"Todo conteúdo disponibilizado pela SmartLuup, incluindo marcas, logotipos, sistemas, códigos, layouts, documentos e materiais institucionais, é protegido pela legislação aplicável.\n\n"

"5. Limitação de Responsabilidade\n\n"

"A SmartLuup emprega esforços razoáveis para manter seus sistemas disponíveis e seguros, mas não garante funcionamento ininterrupto ou livre de falhas.\n\n"

"6. Alterações"

"Estes Termos poderão ser modificados a qualquer momento, sendo as alterações publicadas em nossos canais oficiais.\n\n"

"7. Legislação Aplicável\n\n"

"Os presentes Termos são regidos pelas leis da República Federativa do Brasil.",
    ],
    "Politica de Cookies": [
        "Última atualização: 20 de julho de 2026\n\n"

        "A SmartLuup utiliza cookies e tecnologias semelhantes para melhorar a experiência de navegação dos usuários.\n\n"

        "O que são Cookies?\n\n"

"Cookies são pequenos arquivos armazenados no dispositivo do usuário durante a navegação em nosso site.\n\n"

"Finalidades\n\n"

"Utilizamos cookies para:\n\n"

"* Garantir o funcionamento adequado do site;\n"
"* Melhorar desempenho e segurança;\n"
"* Realizar análises estatísticas;\n"
"* Personalizar conteúdos e experiências.\n"
"* Tipos de Cookies\n"
"* Cookies Essenciais\n"

"Necessários para o funcionamento do site.\n\n"

"Cookies de Desempenho\n\n"

"Permitem analisar a utilização do site para melhorias contínuas.\n\n"

"Cookies Funcionais\n\n"

"Memorizam preferências do usuário.\n\n"

"Cookies de Marketing\n\n"

"Podem ser utilizados para campanhas e divulgação de serviços.\n"

"Gerenciamento"
    ],
    "Conformidade com a LGPD": [
        # LGPD – Lei Geral de Proteção de Dados

"A SmartLuup está comprometida com a proteção dos dados pessoais e com o cumprimento da Lei nº 13.709/2018 (LGPD).\n\n"

## Seus Direitos

"Você pode solicitar:\n\n"

"* Confirmação do tratamento de dados;\n"
"* Acesso aos seus dados pessoais;\n"
"* Correção de informações incorretas;\n"
"* Anonimização ou exclusão dos dados quando aplicável;\n"
"* Portabilidade dos dados;\n"
"* Revogação do consentimento;\n"
"* Informações sobre compartilhamento de dados.\n"

## Como Solicitar

"As solicitações podem ser encaminhadas para:\n\n"

"**E-mail:**\n [privacidade@smartluup.com.br]\n(mailto:privacidade@smartluup.com.br)\n\n"

## Segurança

"A SmartLuup adota medidas administrativas, técnicas e organizacionais para proteger os dados pessoais contra acessos não autorizados, perda, alteração ou divulgação indevida.\n\n"

## Compromisso

"Nos comprometemos a tratar os dados pessoais com transparência, responsabilidade e respeito aos direitos dos titulares.",

    ],
    
}


class LandingPage:
    """Monta toda a landing page one page da SmartLuup."""

    def __init__(self, page: ft.Page):
        """Prepara estado, banco, depoimentos e botao flutuante do agente."""

        self.page = page
        self.metric_values: list[ft.Text] = []
        self.testimonial_index = 0

        # Garante que a tabela de leads exista antes do usuario abrir formulario.
        init_db()

        # Caixa animada usada para trocar os depoimentos automaticamente.
        self.testimonial_box = ft.AnimatedSwitcher(
            content=ft.Container(),
            duration=500,
            transition=ft.AnimatedSwitcherTransition.FADE,
        )

        # Mensagem inicial do chat do agente inteligente.
        self.agent_messages: list[tuple[str, str]] = [
            (
                "agent",
                "Ola! Sou o agente da SmartLuup. Pergunte sobre RPA, Sites, Apps, IA, ERP ou Projetos sob Medida.",
            )
        ]

        # Lista rolavel onde as mensagens do agente aparecem.
        self.agent_messages_column = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)

        # Campo de texto usado pelo visitante para perguntar ao agente.
        self.agent_input = ft.TextField(
            hint_text="Pergunte sobre a SmartLuup...",
            color=theme.WHITE,
            border_color=ft.Colors.with_opacity(0.35, theme.WHITE),
            focused_border_color=theme.GREEN,
            hint_style=ft.TextStyle(color=ft.Colors.with_opacity(0.65, theme.WHITE)),
            border_radius=8,
            multiline=True,
            min_lines=1,
            max_lines=3,
        )

        # Botao flutuante verde que abre o agente SmartLuup.
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.SMART_TOY,
            tooltip="Agente IA SmartLuup",
            bgcolor=theme.GREEN,
            foreground_color=theme.WHITE,
            on_click=lambda _: self.show_ai_agent(),
        )

    def is_mobile(self) -> bool:
        """Retorna True quando a tela esta em tamanho de celular."""

        return bool(self.page.width and self.page.width < 720)

    def build(self) -> ft.Control:
        """Junta todas as secoes da one page em uma coluna unica."""

        return ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=[theme.BG, "#0C0F1A", "#120E1B", theme.BG],
            ),
            content=ft.Column(
                [
                    # Ordem das secoes exibidas na pagina.
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
        """Primeira dobra do site: logo, texto principal, CTA e dashboard."""

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
                src="logonovosmartluup.png",
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
                                color="#d6d6d6",
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
        """Cria um pequeno indicador dentro do dashboard da hero."""

        return ft.Container(
            expand=True,
            padding=10,
            border_radius=ft.BorderRadius(
                top_left=12,
                top_right=12,
                bottom_left=12,
                bottom_right=12,
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
        """Cria uma linha de progresso visual dentro do dashboard."""

        return ft.Container(
            expand=True,
            padding=16,
            border_radius=ft.BorderRadius(
                top_left=12,
                top_right=12,
                bottom_left=12,
                bottom_right=12,
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
        """Monta a seção com os cards de soluções digitais."""

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
        """Monta a seção 'Sobre' com texto institucional e imagem."""

        illustration = GlassCard(
            ft.Container(
                height=400,
                border_radius=ft.BorderRadius(
                    top_left=0,
                    top_right=0,
                    bottom_left=0,
                    bottom_right=0,
                ),
                content=ft.Stack(
                    [
                        ft.Container(),
                        ft.Container(
                            content=ft.Image(
                                src="erp-dashboard-smartluup.png",
                                width=920,
                                height=400,
                                fit=ft.BoxFit.CONTAIN,
                                border_radius=18,
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
                   
                    content=ft.Column(
                        [
                            section_title("Sobre", "A SmartLuup pensa Tecnologia como Resultado"),
                            ft.Text(
                                "A SmartLuup desenvolve soluções tecnologicas que eliminam tarefas repetitivas, reduzem custos operacionais e aumentam a produtividade através da automação, inteligência artificial e desenvolvimento de software sob medida.",
                                color="#d6d6d6",
                                style=theme.body_style(17),
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        spacing=20,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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
        """Monta o portfolio usando os projetos definidos em config.py."""

        project_cards = [
            ft.Container(col={"xs": 12, "md": 4}, content=self.project_card(project))
            for project in PROJECTS
        ]
        return self.section(
            "portfolio",
            ft.Column(
                [
                    section_title("", "Soluções Digitais"),
                    ft.ResponsiveRow(project_cards, spacing=18,
                                      run_spacing=18,
                                        alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=26,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def project_card(self, project: dict) -> ft.Control:
        """Cria o card individual de um projeto do portfolio."""

        image = ft.Container(
            height=100,
            width=100,
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(2, 0, 0, 2),
            border_radius=ft.BorderRadius(
                    top_left=14,
                    top_right=14,
                    bottom_left=14,
                    bottom_right=14,
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
                    GlowButton("Acessar",
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
        """Abre demo interna quando o link comeca com demo:, ou abre URL externa."""

        async def handler(_):
            if str(project.get("link", "")).startswith("demo:"):
                self.show_project_demo(project)
                return

            await self.open_url(project["link"])

        return handler

    def demo_stat(self, value: str, label: str) -> ft.Control:
        """Cria um pequeno card de metrica dentro da demo do projeto."""

        return ft.Container(
            expand=True,
            padding=14,
            border_radius=14,
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
        """Cria uma lista visual de funcionalidades ou beneficios."""

        return ft.Container(
            expand=True,
            padding=18,
            border_radius=14,
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
        """Cria a imagem/mockup conceitual dentro da demo do projeto."""

        return ft.Container(
            height=300,
            padding=18,
            border_radius=14,
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
                        border_radius=14,
                        bgcolor=ft.Colors.with_opacity(0.14, theme.WHITE),
                        content=ft.Column(
                            [
                                ft.Icon(ft.Icons.DASHBOARD_CUSTOMIZE, size=58, color=theme.WHITE),
                                ft.Text(project["demo_titulo"], size=18, weight=ft.FontWeight.W_800, color=theme.WHITE, text_align=ft.TextAlign.CENTER),
                                ft.Text("Demo conceitual SmartLuup", size=13, color=ft.Colors.with_opacity(0.82, theme.WHITE)),
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
        """Abre um overlay com detalhes do projeto selecionado."""

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
                                    content=self.demo_list_card("Benefícios", benefit_items, ft.Icons.TRENDING_UP),
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
        """Cria o balao de mensagem do chat do agente inteligente."""

        is_user = role == "user"
        page_width = self.page.width or 390
        compact_agent = page_width < 1200
        panel_width = 300 if compact_agent else 520
        messages_content_width = panel_width - (52 if compact_agent else 84)
        bubble_width = messages_content_width - 18 if compact_agent else 420
        wrapped_text = "\n".join(textwrap.wrap(text, width=24 if compact_agent else 54))
        return ft.Container(
            width=messages_content_width,
            alignment=ft.Alignment(1, 0) if is_user else ft.Alignment(-1, 0),
            clip_behavior=ft.ClipBehavior.HARD_EDGE,
            content=ft.Container(
                    width=bubble_width,
                    padding=8,
                    border_radius=16,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    bgcolor=theme.GREEN if is_user else ft.Colors.with_opacity(0.10, theme.WHITE),
                    border=None if is_user else ft.Border.all(1, ft.Colors.with_opacity(0.16, theme.WHITE)),
                    content=ft.Text(
                        wrapped_text,
                        width=bubble_width - 24,
                        color=theme.WHITE,
                        size=13 if compact_agent else 14,
                        no_wrap=False,
                        max_lines=10,
                        overflow=ft.TextOverflow.CLIP,
                    ),
                ),
        )

    def refresh_agent_messages(self):
        """Recria a lista visual de mensagens do agente."""

        self.agent_messages_column.controls = [
            self.agent_bubble(role, message)
            for role, message in self.agent_messages
        ]

    def show_ai_agent(self):
        """Abre a janela flutuante do agente inteligente."""

        page_width = self.page.width or 390
        page_height = self.page.height or 780
        compact_agent = page_width < 1200
        panel_width = 300 if compact_agent else 520
        message_area_width = panel_width - (20 if compact_agent else 36)
        messages_content_width = message_area_width - (16 if compact_agent else 24)
        panel_height = min(560, page_height - 120) if compact_agent else 620
        self.agent_messages_column.width = messages_content_width
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

            answer = await asyncio.to_thread(ask_smartluup_ai, question)
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
                border_radius=20,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SMART_TOY, color=theme.GREEN, size=24),
                                ft.Text(
                                    "Agente SmartLuup",
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
                            width=message_area_width,
                            expand=True,
                            padding=8 if compact_agent else 12,
                            border_radius=16,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            bgcolor=ft.Colors.with_opacity(0.06, theme.WHITE),
                            content=ft.Container(
                                width=messages_content_width,
                                clip_behavior=ft.ClipBehavior.HARD_EDGE,
                                content=self.agent_messages_column,
                            ),
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
                            "Respostas geradas por IA. Para proposta comercial, solicite um Orçamento.",
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
        """Monta a secao de numeros animados da empresa."""

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
        """Monta a secao de diferenciais competitivos."""

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
        """Monta a secao de depoimentos com slider automatico."""

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
        """Cria o card visual de um depoimento."""

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
        """Monta a chamada final para o WhatsApp."""

        mobile = self.is_mobile()
        return self.section(
            "cta",
            GlassCard(
                ft.Column(
                    [
                        ft.Text("Pronto para Automatizar seu Negócio?", style=theme.title_style(29 if mobile else 42), text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            "Vamos Desenhar um Fluxo mais Rápido, Inteligente e Lucrativo para sua Empresa.",
                            color="#d6d6d6",
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

    def show_policy_modal(self, title: str):
        """Abre um painel com o conteudo da politica escolhida no rodape."""

        mobile = self.is_mobile()
        policy_items = PRIVACY_POLICIES.get(title, [])

        def close_policy(_=None):
            if policy_overlay in self.page.overlay:
                self.page.overlay.remove(policy_overlay)
            self.page.update()

        policy_overlay = ft.Container(
            expand=True,
            bgcolor=ft.Colors.with_opacity(0.84, "#020617"),
            alignment=ft.Alignment(0, 0),
            padding=14 if mobile else 24,
            content=ft.Container(
                width=345 if mobile else 760,
                height=560 if mobile else None,
                padding=18 if mobile else 26,
                border_radius=18,
                bgcolor="#0F172A",
                border=ft.Border.all(1, ft.Colors.with_opacity(0.22, theme.WHITE)),
                shadow=theme.soft_shadow(theme.BLUE, opacity=0.14, blur=34),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.SHIELD, size=24, color=theme.GREEN),
                                ft.Text(
                                    title,
                                    size=22 if mobile else 28,
                                    weight=ft.FontWeight.W_800,
                                    color=theme.WHITE,
                                    expand=True,
                                ),
                                ft.IconButton(ft.Icons.CLOSE, icon_color=theme.WHITE, on_click=close_policy),
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        ft.Divider(color=ft.Colors.with_opacity(0.16, theme.WHITE)),
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=18, color=theme.GREEN),
                                        ft.Text(
                                            item,
                                            color=theme.WHITE,
                                            size=14 if mobile else 16,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                )
                                for item in policy_items
                            ],
                            spacing=14,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        ft.Text(
                            "Conteúdo informativo. Para uma solicitação formal, use os canais oficiais da SmartLuup.",
                            color=ft.Colors.with_opacity(0.70, theme.WHITE),
                            size=12 if mobile else 13,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                    spacing=14,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        )

        self.page.overlay.append(policy_overlay)
        self.page.update()

    def footer(self) -> ft.Control:
        """Monta o rodape com links externos e contatos."""

        mobile = self.is_mobile()
        links = [
            ("Email", f"mailto:{CONTACT.email}"),
            ("WhatsApp", CONTACT.whatsapp),
            ("Instagram", CONTACT.instagram),
            ("LinkedIn", CONTACT.linkedin),
            ("GitHub", CONTACT.github),
        ]

        def policy_link(label: str) -> ft.Container:
            return ft.Container(
                on_click=lambda _, policy_title=label: self.show_policy_modal(policy_title),
                padding=ft.Padding(0, 2, 0, 2),
                content=ft.Text(
                    label,
                    color=theme.BLUE,
                    size=14 if mobile else 15,
                    text_align=ft.TextAlign.CENTER,
                ),
            )

        policy_items = list(PRIVACY_POLICIES.keys())
        policy_controls = []
        for index, label in enumerate(policy_items):
            policy_controls.append(policy_link(label))
            if index < len(policy_items) - 1:
                policy_controls.append(ft.Text("|", color=theme.WHITE, size=14))

        return ft.Container(
            padding=ft.Padding(0, 20 if mobile else 28, 0, 26 if mobile else 34),
            content=max_width(
                ft.Column(
                    [
                        ft.Text("SmartLuup", size=26, weight=ft.FontWeight.W_800,
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER),
                        ft.Text("Automação • IA • Sites • Aplicativos",
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER,
                                 width=310 if mobile else None),
                        ft.Text("© 2024 SmartLuup. Todos os direitos reservados",
                                 color=theme.WHITE, text_align=ft.TextAlign.CENTER,
                                 width=310 if mobile else None),
                        ft.Text(
                            "Desenvolvido por SmartLuup. Valter Lira. Tecnologia Python",
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
                        ft.Container(height=6 if mobile else 10),
                        ft.Text(
                            "🔒 Segurança e Privacidade",
                            size=15 if mobile else 17,
                            weight=ft.FontWeight.W_800,
                            color=theme.WHITE,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Container(
                            width=330 if mobile else 760,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Row(
                                policy_controls,
                                wrap=True,
                                spacing=8,
                                run_spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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
        """Aplica espacamento padrao e chave de scroll em cada secao."""

        mobile = self.is_mobile()
        return ft.Container(
            key=key,
            padding=ft.Padding(0, 28 if mobile else 46, 0, 28 if mobile else 46),
            content=max_width(content, padding=18 if mobile else 56),
        )

    def show_budget_form_handler(self):
        """Cria o manipulador de clique que abre o formulario de orcamento."""

        async def handler(_):
            self.show_budget_form()

        return handler

    def form_field(self, label: str, multiline: bool = False) -> ft.Container:
        """Cria um campo de formulario com o visual padrao."""

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
        """Envolve campos e dropdowns com borda verde quando recebem foco."""

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
        """Versao antiga do formulario em dialog. Mantida como referencia."""

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
                            "Preencha as informações para a SmartLuup entender seu Negócio e entrar em contato.",
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
            print("Clique recebido no botão Salvar lead")
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
        """Versao antiga do formulario em overlay. Mantida como referencia."""

        nome = self.form_field("Seu nome")
        empresa = self.form_field("Nome da empresa")
        whatsapp = self.form_field("WhatsApp")
        email = self.form_field("Email")
        segmento = self.form_field("Segmento do negócio")
        objetivo = self.form_field("Qual problema você quer resolver?", multiline=True)
        detalhes = self.form_field("Conte mais detalhes do projeto", multiline=True)
        tipo_projeto = ft.Dropdown(
            label="Qual projeto de tecnologia você quer fazer?",
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
            print("Clique recebido no botão Salvar lead")
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
                                    "Voltar para página",
                                    icon=ft.Icons.ARROW_BACK,
                                    on_click=close_form,
                                    style=ft.ButtonStyle(color=theme.GREEN),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.Text(
                            "Preencha as informações para a SmartLuup entender seu negócio e entrar em contato.",
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
        """Abre uma URL externa no navegador."""

        result = self.page.launch_url(url)
        if inspect.isawaitable(result):
            await result

    async def scroll_to(self, key: str):
        """Rola a pagina ate uma secao pela chave informada."""

        await self.page.scroll_to(scroll_key=key,
                                   duration=700, 
                                   curve=ft.AnimationCurve.EASE_IN_OUT)

    def open_url_handler(self, url: str):
        """Cria um evento de clique para abrir URL externa."""

        async def handler(_):
            await self.open_url(url)

        return handler

    def scroll_handler(self, key: str):
        """Cria um evento de clique para rolar ate uma secao."""

        async def handler(_):
            await self.scroll_to(key)

        return handler

    def show_budget_form(self):
        """Formulario principal de captacao de leads/orcamentos."""

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
            print("Clique recebido no botão Salvar lead")
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
                                ft.Text("Solicitar Orçamento", color=theme.WHITE, size=21, weight=ft.FontWeight.W_800),
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
        """Inicia animacoes que rodam depois que a pagina carregou."""

        threading.Thread(target=self._animate_metrics, daemon=True).start()
        threading.Thread(target=self._rotate_testimonials, daemon=True).start()

    def _animate_metrics(self):
        """Anima os numeros da secao de metricas progressivamente."""

        time.sleep(0.65)
        for step in range(1, 41):
            for idx, (_, target, prefix, suffix) in enumerate(METRICS):
                current = round(target * step / 40)
                self.metric_values[idx].value = f"{prefix}{current}{suffix}"
            self.page.update()
            time.sleep(0.035)

    def _rotate_testimonials(self):
        """Troca os depoimentos automaticamente em loop."""

        while True:
            time.sleep(4.2)
            self.testimonial_index = (self.testimonial_index + 1) % len(TESTIMONIALS)
            self.testimonial_box.content = self.testimonial_card(TESTIMONIALS[self.testimonial_index])
            self.page.update()
