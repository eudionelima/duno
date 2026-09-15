"""modules/api_versioning/source/low.py — DUNO source view."""
from core.database import get_db


def handle(version: str) -> list:
    """Low: retorna todos os tokens de qualquer versão sem autenticação."""
    db = get_db()
    rows = db.execute("SELECT * FROM api_tokens").fetchall()
    return [dict(r) for r in rows]
