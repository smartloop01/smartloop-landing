from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = Path(__file__).with_name("leads.db")
DB_TIMEOUT_SECONDS = 2


def connect_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT_SECONDS)
    conn.execute("PRAGMA busy_timeout = 2000")
    conn.execute("PRAGMA journal_mode = WAL")
    return conn


def init_db() -> None:
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
    print(f"Tentando salvar lead em {DB_PATH}")
    print("Preparando tabela de leads...")
    init_db()
    print("Tabela pronta. Preparando dados...")
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

    with connect_db() as conn:
        print("Inserindo lead no SQLite...")
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
