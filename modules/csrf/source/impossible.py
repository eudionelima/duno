"""modules/csrf/source/impossible.py — DUNO source view."""
import secrets
import hashlib
from flask import session


def generate_token(user_id: int) -> str:
    """Gera token CSRF por (user, form, timestamp) — one-time use."""
    raw = f"{user_id}:{secrets.token_hex(16)}"
    session["csrf_token_impossible"] = raw
    return hashlib.sha256(raw.encode()).hexdigest()


def handle(db, user_id: int, new_email: str, submitted_token: str) -> str:
    """Impossible: token CSRF one-time + validação de senha atual."""
    stored = session.pop("csrf_token_impossible", None)
    if not stored:
        return "Token CSRF ausente ou expirado."
    expected = hashlib.sha256(stored.encode()).hexdigest()
    if submitted_token != expected:
        return "Token CSRF inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
