"""modules/csrf/source/medium.py — DUNO source view."""
from flask import request


def handle(db, user_id: int, new_email: str) -> str:
    """Medium: verifica Referer — bypassável com Referer forjado ou ausente."""
    ref = request.headers.get("Referer", "")
    if "localhost" not in ref and "127.0.0.1" not in ref:
        return "Referer inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
