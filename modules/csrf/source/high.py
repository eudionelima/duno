"""modules/csrf/source/high.py — DUNO source view."""
from flask import session


def handle(db, user_id: int, new_email: str, submitted_token: str) -> str:
    """High: token CSRF válido mas implementação tem falha — token fixo por sessão, não por form."""
    expected = session.get("csrf_token_csrf", "")
    if not expected or submitted_token != expected:
        return "Token CSRF inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
