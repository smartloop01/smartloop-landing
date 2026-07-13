from __future__ import annotations

import os


SMARTLOOP_CONTEXT = """
Voce e o agente inteligente da SmartLoop.
A SmartLoop cria solucões para empresas com Automação RPA, Desenvolvimento de Sites,
Aplicativos Mobile e Web, Inteligencia Artificial.

Projetos demonstrados:
- SmartLoop ERP: sistema de gestao empresarial com dashboards, financeiro, vendas, estoque e relatorios.
- SmartLoop RPA: robos para automatizar tarefas repetitivas, integracoes, relatorios e rotinas administrativas.
- AI Sales Copilot: assistente de IA para qualificar leads, resumir conversas e priorizar oportunidades comerciais.

Objetivo do atendimento:
- Responder perguntas sobre a SmartLoop.
- Explicar solucoes de forma simples e consultiva.
- Incentivar o visitante a solicitar um orcamento quando houver interesse.
- Nao inventar preco fixo. Diga que depende do escopo, prazo e complexidade.
Se nao souber a resposta, diga que pode ajudar em modo local e forneca uma resposta padrao com informacoes uteis sobre a SmartLoop.
"""


FALLBACK_ANSWERS = {
    "rpa": "A SmartLoop cria automacoes RPA para reduzir tarefas repetitivas, integrar sistemas, gerar relatorios e diminuir erros operacionais.",
    "site": "A SmartLoop desenvolve sites, landing pages e sistemas web com foco em performance, visual profissional e captacao de clientes.",
    "app": "A SmartLoop cria aplicativos mobile e web sob medida para operacao, atendimento, vendas e produtividade empresarial.",
    "ia": "A SmartLoop aplica IA em atendimento, vendas, analise de dados, copilotos internos e automacoes inteligentes.",
    "erp": "O SmartLoop ERP e uma demonstracao de sistema de gestao com clientes, vendas, financeiro, estoque, relatorios e dashboards.",
    "preco": "O investimento depende do escopo, prazo e complexidade. O ideal e solicitar um orcamento para a SmartLoop entender seu negocio.",
    "orcamento": "Para solicitar um orcamento, clique em 'Solicitar Orcamento' ou fale pelo WhatsApp da SmartLoop.",
}


def fallback_answer(question: str) -> str:
    normalized = question.lower()
    for keyword, answer in FALLBACK_ANSWERS.items():
        if keyword in normalized:
            return answer

    return (
        "A SmartLoop ajuda empresas com automacao RPA, sites, aplicativos, IA e solucoes "
        "para aumentar produtividade. Me diga qual desafio voce quer resolver que eu te "
        "explico o melhor caminho."
    )


def ask_smartloop_ai(question: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("Agente SmartLoop: OPENAI_API_KEY nao encontrada. Usando modo local.")
        return fallback_answer(question)

    try:
        from openai import OpenAI

        print(f"Agente SmartLoop: usando OpenAI com modelo {model}.")
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SMARTLOOP_CONTEXT},
                {"role": "user", "content": question},
            ],
            temperature=0.35,
            max_tokens=420,
        )
        return response.choices[0].message.content.strip()
    except Exception as error:
        return (
            "Nao consegui conectar com a IA agora, mas posso ajudar em modo local. "
            f"Detalhe tecnico: {error}. "
            + fallback_answer(question)
        )
