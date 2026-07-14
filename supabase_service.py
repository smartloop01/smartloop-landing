from __future__ import annotations

import os


SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "leads")


def supabase_is_configured() -> bool:
    """Confere se as variaveis obrigatorias do Supabase estao configuradas."""

    return bool(os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"))


def get_supabase_client():
    """Cria o client do Supabase somente quando for necessario."""

    from supabase import create_client

    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_KEY"]
    return create_client(url, key)


def save_lead_supabase(fields: dict[str, str]) -> int:
    """Salva o lead na tabela do Supabase e retorna o ID criado."""

    print(f"Tentando salvar lead no Supabase, tabela {SUPABASE_TABLE}...")
    response = (
        get_supabase_client()
        .table(SUPABASE_TABLE)
        .insert(fields)
        .select("id")
        .execute()
    )

    data = response.data or []
    if not data:
        raise RuntimeError("Supabase nao retornou o lead inserido.")

    lead_id = int(data[0]["id"])
    print(f"Supabase confirmou o lead #{lead_id}")
    return lead_id
