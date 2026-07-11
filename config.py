from dataclasses import dataclass


@dataclass(frozen=True)
class ContactConfig:
    email: str = "smartloopgmail@gmail.com"
    whatsapp: str = "https://wa.me/5516991327011?text=Olá,%20quero%20um%20orçamento%20para%20minha%20empresa!"
    instagram: str = "https://instagram.com/smartloop_1"
    linkedin: str = "https://linkedin.com/in/valter-lira"
    github: str = "https://github.com/smartloop01"


CONTACT = ContactConfig()


PROJECTS = [
    {
        "nome": "SmartLoop ERP",
        "descricao": "Sistema de gestão empresarial com paineis, indicadores e fluxos integrados.",
        "categoria": "Web",
        "link": "https://site.com",
        "imagem": "ERP",
    },
    {
        "nome": "SmartLoop RPA",
        "descricao": "Automação de processos repetitivos para operacões financeiras e administrativas.",
        "categoria": "Automação",
        "link": "https://site.com",
        "imagem": "RPA",
    },
    {
        "nome": "AI Sales Copilot",
        "descricao": "Assistente inteligente para qualificar leads, resumir conversas e priorizar vendas.",
        "categoria": "IA",
        "link": "https://site.com",
        "imagem": "AI",
    },
]


PROJECT_DEMOS = {
    "SmartLoop ERP": {
        "link": "demo:erp",
        "demo_titulo": "ERP inteligente para gestao empresarial",
        "demo_resumo": "Uma central para acompanhar clientes, vendas, financeiro, estoque e indicadores em tempo real.",
        "demo_metricas": [
            ("+38%", "produtividade"),
            ("-42%", "retrabalho"),
            ("24/7", "visao do negocio"),
        ],
        "demo_funcionalidades": [
            "Dashboard executivo com KPIs em tempo real",
            "Cadastro de clientes, produtos e usuarios",
            "Controle financeiro, vendas e estoque",
            "Relatorios automaticos para tomada de decisao",
        ],
        "demo_beneficios": [
            "Mais controle operacional",
            "Menos planilhas soltas",
            "Gestao centralizada",
        ],
    },
    "SmartLoop RPA": {
        "link": "demo:rpa",
        "demo_titulo": "Robos para automatizar processos repetitivos",
        "demo_resumo": "Automacoes para executar tarefas operacionais, integrar sistemas e reduzir tempo perdido em rotinas manuais.",
        "demo_metricas": [
            ("100k+", "horas automatizadas"),
            ("87%", "menos retrabalho"),
            ("24/7", "execucao ativa"),
        ],
        "demo_funcionalidades": [
            "Leitura e preenchimento automatico de sistemas",
            "Geracao de relatorios e envio por email",
            "Integracao entre planilhas, ERPs e portais",
            "Monitoramento de falhas e logs de execucao",
        ],
        "demo_beneficios": [
            "Equipe livre de tarefas repetitivas",
            "Processos mais rapidos",
            "Menos erros manuais",
        ],
    },
    "AI Sales Copilot": {
        "link": "demo:ai-sales",
        "demo_titulo": "Copiloto de IA para times comerciais",
        "demo_resumo": "Um assistente para analisar leads, resumir atendimentos, sugerir proximas acoes e acelerar o ciclo de vendas.",
        "demo_metricas": [
            ("+31%", "conversao"),
            ("-55%", "tempo de resposta"),
            ("98%", "priorizacao"),
        ],
        "demo_funcionalidades": [
            "Resumo automatico de conversas comerciais",
            "Classificacao de leads por potencial de compra",
            "Sugestao de proximas mensagens e follow-ups",
            "Painel de oportunidades e alertas inteligentes",
        ],
        "demo_beneficios": [
            "Vendas mais consultivas",
            "Atendimento mais rapido",
            "Pipeline mais organizado",
        ],
    },
}


for project in PROJECTS:
    project.update(PROJECT_DEMOS.get(project["nome"], {}))


TESTIMONIALS = [
    {
        "nome": "Marina Costa",
        "cargo": "Diretora de Operacoes",
        "texto": "A SmartLoop automatizou rotinas criticas e liberou nosso time para pensar no crescimento.",
        "iniciais": "MC",
    },
    {
        "nome": "Rafael Mendes",
        "cargo": "CEO, NovaLog",
        "texto": "O projeto ficou elegante, rapido e muito alinhado com os processos da empresa.",
        "iniciais": "RM",
    },
    {
        "nome": "Bianca Torres",
        "cargo": "Head de Produto",
        "texto": "Ganhamos previsibilidade, integracao e uma experiência digital muito superior.",
        "iniciais": "BT",
    },
]
