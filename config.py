from dataclasses import dataclass


# Dados de contato usados nos botoes e no rodape.
# Para trocar links do site, edite os valores abaixo.
@dataclass(frozen=True)
class ContactConfig:
    email: str = "smartloopgmail@gmail.com"
    whatsapp: str = "https://wa.me/5516991327011?text=Ola%2C%20quero%20um%20orcamento%20para%20minha%20empresa"
    instagram: str = "https://www.instagram.com/smartloop_1"
    linkedin: str = "https://www.linkedin.com/in/valter-lira"
    github: str = "https://github.com/smartloop01"


CONTACT = ContactConfig()


# Lista principal de projetos exibidos na secao Portfolio.
# Importante: mantenha os nomes das chaves exatamente assim:
# "nome", "descricao", "categoria", "link" e "imagem".
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
        "descricao": "Automacão de processos repetitivos para operacões financeiras e administrativas.",
        "categoria": "Automacão",
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


# Dados extras das paginas demonstrativas de cada projeto.
# A chave principal precisa ter o mesmo nome usado em PROJECTS["nome"].
PROJECT_DEMOS = {
    "SmartLoop ERP": {
        "link": "demo:erp",
        "demo_titulo": "ERP inteligente para gestão empresarial",
        "demo_resumo": "Uma central para acompanhar clientes, vendas, financeiro, estoque e indicadores em tempo real.",
        "demo_metricas": [
            ("+38%", "produtividade"),
            ("-42%", "retrabalho"),
            ("24/7", "visao do negócio"),
        ],
        "demo_funcionalidades": [
            "Dashboard executivo com KPIs em tempo real",
            "Cadastro de clientes, produtos e usuarios",
            "Controle financeiro, vendas e estoque",
            "Relatórios automaticos para tomada de decisão",
        ],
        "demo_beneficios": [
            "Mais controle operacional",
            "Menos planilhas soltas",
            "Gestão centralizada",
        ],
    },
    "SmartLoop RPA": {
        "link": "demo:rpa",
        "demo_titulo": "Robos para automatizar processos repetitivos",
        "demo_resumo": "Automacões para executar tarefas operacionais, integrar sistemas e reduzir tempo perdido em rotinas manuais.",
        "demo_metricas": [
            ("100k+", "Horas automatizadas"),
            ("87%", "Menos retrabalho"),
            ("24/7", "Execucão ativa"),
        ],
        "demo_funcionalidades": [
            "Leitura e preenchimento automatico de sistemas",
            "Geracão de relatorios e envio por email",
            "Integracão entre planilhas, ERPs e portais",
            "Monitoramento de falhas e logs de execucão",
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
        "demo_resumo": "Um assistente para analisar leads, resumir atendimentos, sugerir proximas acões e acelerar o ciclo de vendas.",
        "demo_metricas": [
            ("+31%", "Conversão"),
            ("-55%", "Tempo de resposta"),
            ("98%", "Priorizacao"),
        ],
        "demo_funcionalidades": [
            "Resumo automatico de conversas comerciais",
            "Classificacão de leads por potencial de compra",
            "Sugestão de proximas mensagens e follow-ups",
            "Painel de oportunidades e alertas inteligentes",
        ],
        "demo_beneficios": [
            "Vendas mais consultivas",
            "Atendimento mais rapido",
            "Pipeline mais organizado",
        ],
    },
}


# Junta os dados basicos de PROJECTS com as informacoes extras de PROJECT_DEMOS.
# Assim cada card do portfolio ja recebe link, metricas, beneficios e mockup.
for project in PROJECTS:
    project.update(PROJECT_DEMOS.get(project["nome"], {}))


# Depoimentos exibidos no slider automatico.
# Cada item tem nome, cargo, texto e iniciais para o avatar circular.
TESTIMONIALS = [
    {
        "nome": "Cristina Costa",
        "cargo": "Diretora de Operacões",
        "texto": "A SmartLoop automatizou rotinas criticas e liberou nosso time para pensar no crescimento.",
        "iniciais": "CC",
    },
    {
        "nome": "Raphael Mendes",
        "cargo": "CEO, NovaLog",
        "texto": "O projeto ficou elegante, rapido e muito alinhado com os processos da empresa.",
        "iniciais": "RM",
    },
    {
        "nome": "Cecilia Torres",
        "cargo": "Head de Produto",
        "texto": "Ganhamos previsibilidade, integracão e uma experiencia digital muito superior.",
        "iniciais": "CT",
    },
]
