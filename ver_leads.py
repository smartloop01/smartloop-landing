import sqlite3

from lead_service import DB_PATH, init_db


init_db()

with sqlite3.connect(DB_PATH) as conn:
    conn.row_factory = sqlite3.Row
    leads = conn.execute(
        """
        SELECT id, criado_em, nome, empresa, whatsapp, tipo_projeto, objetivo
        FROM leads
        ORDER BY id DESC
        """
    ).fetchall()

if not leads:
    print("Nenhum lead cadastrado ainda.")
else:
    for lead in leads:
        print("-" * 60)
        print(f"Codigo: {lead['id']}")
        print(f"Data: {lead['criado_em']}")
        print(f"Nome: {lead['nome']}")
        print(f"Empresa: {lead['empresa']}")
        print(f"WhatsApp: {lead['whatsapp']}")
        print(f"Projeto: {lead['tipo_projeto']}")
        print(f"Objetivo: {lead['objetivo']}")
