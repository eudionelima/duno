"""modules/sqli_blind/source/high.py — DUNO source view."""
import time


def handle(db, user_id: str) -> str:
    """High: time-based — usa sqlite3 heavy query para inferir dados."""
    query = (
        f"SELECT CASE WHEN (SELECT COUNT(*) FROM users WHERE id={user_id})>0 "
        "THEN (SELECT COUNT(*) FROM sqlite_master) ELSE 0 END"
    )
    try:
        db.execute(query)
        return "Usuário existe."
    except Exception as e:
        return f"Erro: {e}"
