"""modules/sqli_blind/source/medium.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Medium: sanitiza aspas mas não previne injeção numérica."""
    user_id = user_id.replace("'", "").replace('"', "")
    query = f"SELECT COUNT(*) FROM users WHERE id = {user_id}"
    try:
        count = db.execute(query).fetchone()[0]
        return "Usuário existe." if count > 0 else "Usuário não encontrado."
    except Exception as e:
        return f"Erro: {e}"
