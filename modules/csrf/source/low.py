"""modules/csrf/source/low.py — DUNO source view."""


def handle(db, user_id: int, new_email: str) -> str:
    """Low: altera e-mail sem token CSRF — qualquer site pode forjar a requisição."""
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
