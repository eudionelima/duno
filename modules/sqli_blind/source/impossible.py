"""modules/sqli_blind/source/impossible.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Impossible: prepared statement + validação de tipo inteiro."""
    try:
        uid = int(user_id)
    except ValueError:
        return "ID inválido."
    count = db.execute(
        "SELECT COUNT(*) FROM users WHERE id=?", (uid,)
    ).fetchone()[0]
    return "Usuário existe." if count > 0 else "Usuário não encontrado."
