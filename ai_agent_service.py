from __future__ import annotations

import os


# Contexto principal enviado para a OpenAI.
# Voce pode editar o texto entre as aspas triplas.
SMARTLOOP_CONTEXT = """
Você é o agente inteligente da SmartLoop.
A SmartLoop cria solucões para empresas com Automação RPA, Desenvolvimento de Sites,
Aplicativos Mobile e Web, Inteligencia Artificial.

Projetos demonstrados:
- SmartLoop ERP: Sistema de gestão empresarial com dashboards, financeiro, vendas, estoque e relatorios.
- SmartLoop RPA: Robos para automatizar tarefas repetitivas, integracões, relatorios e rotinas administrativas.
- AI Sales Copilot: Assistente de IA para qualificar leads, resumir conversas e priorizar oportunidades comerciais.

Objetivo do atendimento:
- Responder perguntas sobre a SmartLoop.
- Explicar solucões de forma simples e consultiva.
- Incentivar o visitante a solicitar um orçamento quando houver interesse.
- Nao inventar preço fixo. Diga que depende do escopo, prazo e complexidade.
Se nao souber a resposta, diga que pode ajudar em modo local e forneca uma resposta padrão com informacões uteis sobre a SmartLoop.
"""


# Respostas locais usadas quando a OpenAI nao esta configurada ou falha.
# Cada chave e uma palavra que o sistema procura na pergunta do visitante.
FALLBACK_ANSWERS = {
    "rpa": "A SmartLoop cria automacões RPA para reduzir tarefas repetitivas, integrar sistemas, gerar relatorios e diminuir erros operacionais.",
    "site": "A SmartLoop desenvolve sites, landing pages e sistemas web com foco em performance, visual profissional e captacão de clientes.",
    "app": "A SmartLoop cria aplicativos mobile e web sob medida para operacão, atendimento, vendas e produtividade empresarial.",
    "ia": "A SmartLoop aplica IA em atendimento, vendas, analise de dados, copilotos internos e automacões inteligentes.",
    "erp": "O SmartLoop ERP e uma demonstracão de sistema de gestão com clientes, vendas, financeiro, estoque, relatorios e dashboards.",
    "preco": "O investimento depende do escopo, prazo e complexidade. O ideal e solicitar um orçamento para a SmartLoop entender seu negocio.",
    "orçamento": "Para solicitar um orçamento, clique em 'Solicitar Orçamento' ou fale pelo WhatsApp da SmartLoop.",
}


def fallback_answer(question: str) -> str:
    """Gera uma resposta simples sem usar OpenAI."""

    normalized = question.lower()

    # Procura uma palavra-chave conhecida dentro da pergunta.
    for keyword, answer in FALLBACK_ANSWERS.items():
        if keyword in normalized:
            return answer

    # Resposta padrao quando nenhuma palavra-chave foi encontrada.
    return (
        "A SmartLoop ajuda empresas com automacão RPA, sites, aplicativos, IA e solucões "
        "para aumentar produtividade. Me diga qual desafio voce quer resolver que eu te "
        "explico o melhor caminho."
    )


def ask_smartloop_ai(question: str) -> str:
    """Responde com OpenAI quando possivel; caso contrario usa fallback local."""

    # A chave da OpenAI deve ficar no ambiente, nunca escrita no codigo.
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("Agente SmartLoop: OPENAI_API_KEY nao encontrada. Usando modo local.")
        return fallback_answer(question)

    try:
        from openai import OpenAI

        # Chamada principal para o modelo configurado.
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
        # Se a API falhar, o visitante ainda recebe uma resposta util.
        return (
            "Nao consegui conectar com a IA agora, mas posso ajudar em modo local. "
            f"Detalhe tecnico: {error}. "
            + fallback_answer(question)
        )
