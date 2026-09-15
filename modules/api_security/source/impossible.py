"""modules/api_security/source/impossible.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """Impossible: verifica ownership estritamente + rate limit implícito via audit_log."""
    uid = session.get("user_id")
    if not uid or uid != user_id:
        return {"error": "Acesso negado."}
    db = get_db()
    row = db.execute("SELECT id, username FROM users WHERE id=?", (uid,)).fetchone()
    return dict(row) if row else {}
