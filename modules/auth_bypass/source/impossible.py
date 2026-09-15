"""modules/auth_bypass/source/impossible.py — DUNO source view."""
from core.database import get_db






from flask import session


def check_access(user: dict) -> bool:
    """Impossible: verifica role diretamente no banco — sem confiar em sessão/cookie."""
    uid = session.get("user_id")
    if not uid:
        return False
    db = get_db()
    row = db.execute("SELECT role FROM users WHERE id=?", (uid,)).fetchone()
    return row is not None and row["role"] == "admin"
