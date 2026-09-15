"""modules/api_security/source/medium.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """Medium: verifica autenticação mas não ownership — IDOR autenticado."""
    uid = session.get("user_id")
    if not uid:
        return {"error": "Não autenticado."}
    db = get_db()
    row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else {}
