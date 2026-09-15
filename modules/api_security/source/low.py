"""modules/api_security/source/low.py — DUNO source view."""
from core.database import get_db


def get_user(user_id: int) -> dict:
    """Low: IDOR — sem verificação de propriedade. Acesse /api/users/<any_id>."""
    db = get_db()
    row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else {}
