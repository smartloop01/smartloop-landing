from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from supabase_service import save_lead_supabase, supabase_is_configured


# Banco SQLite local. O arquivo leads.db fica nesta mesma pasta.
DB_PATH = Path(__file__).with_name("leads.db")
DB_TIMEOUT_SECONDS = 2


def connect_db() -> sqlite3.Connection:
    """Abre uma conexao com o banco de leads."""

    conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT_SECONDS)

    # busy_timeout ajuda quando duas acoes tentam acessar o banco ao mesmo tempo.
    conn.execute("PRAGMA busy_timeout = 2000")

    # WAL melhora a estabilidade do SQLite enquanto o app esta rodando.
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db() -> None:
    """Cria a tabela de leads caso ela ainda nao exista."""

    with connect_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                empresa TEXT NOT NULL,
                whatsapp TEXT NOT NULL,
                email TEXT,
                segmento TEXT,
                tipo_projeto TEXT NOT NULL,
                objetivo TEXT NOT NULL,
                prazo TEXT,
                orcamento TEXT,
                detalhes TEXT,
                criado_em TEXT NOT NULL
            )
            """
        )


def save_lead(data: dict[str, str]) -> int:
    """Salva o lead no Supabase quando configurado; senao usa SQLite local."""

    print("Preparando dados do lead...")

    # Padroniza todos os campos antes de salvar no banco.
    fields = {
        "nome": data.get("nome", "").strip(),
        "empresa": data.get("empresa", "").strip(),
        "whatsapp": data.get("whatsapp", "").strip(),
        "email": data.get("email", "").strip(),
        "segmento": data.get("segmento", "").strip(),
        "tipo_projeto": data.get("tipo_projeto", "").strip(),
        "objetivo": data.get("objetivo", "").strip(),
        "prazo": data.get("prazo", "").strip(),
        "orcamento": data.get("orcamento", "").strip(),
        "detalhes": data.get("detalhes", "").strip(),
        "criado_em": datetime.now().isoformat(timespec="seconds"),
    }

    if supabase_is_configured():
        try:
            return save_lead_supabase(fields)
        except Exception as error:
            print(f"Erro ao salvar no Supabase: {error}")
            print("Usando SQLite local como backup.")

    print(f"Tentando salvar lead em {DB_PATH}")
    print("Preparando tabela de leads...")
    init_db()
    print("Tabela pronta.")

    with connect_db() as conn:
        print("Inserindo lead no SQLite...")

        # Os parametros com dois pontos (:nome, :empresa...) pegam os valores
        # do dicionario fields de forma segura.
        cursor = conn.execute(
            """
            INSERT INTO leads (
                nome, empresa, whatsapp, email, segmento, tipo_projeto,
                objetivo, prazo, orcamento, detalhes, criado_em
            )
            VALUES (
                :nome, :empresa, :whatsapp, :email, :segmento, :tipo_projeto,
                :objetivo, :prazo, :orcamento, :detalhes, :criado_em
            )
            """,
            fields,
        )
        conn.commit()
        lead_id = int(cursor.lastrowid)
        print(f"SQLite confirmou o lead #{lead_id}")
        return lead_id
