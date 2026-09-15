"""modules/api_versioning/source/impossible.py — DUNO source view."""
from core.database import get_db
from flask import session


def handle() -> list:
    """Impossible: v1 desativado, filtra por user_id da sessão, sem campos sensíveis."""
    uid = session.get("user_id")
    db = get_db()
    rows = db.execute(
        "SELECT id, version FROM api_tokens WHERE user_id=? AND version='v2'", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
