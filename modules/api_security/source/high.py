"""modules/api_security/source/high.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """High: verifica ownership para users mas admin pode ver todos."""
    uid = session.get("user_id")
    if not uid:
        return {"error": "Não autenticado."}
    role = session.get("role")
    if role == "admin" or uid == user_id:
        db = get_db()
        row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(row) if row else {}
    return {"error": "Acesso negado."}
