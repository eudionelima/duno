"""modules/sqli_blind/source/low.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Low: boolean-based blind — só retorna 'existe' ou 'não existe'."""
    query = f"SELECT COUNT(*) FROM users WHERE id = {user_id}"
    try:
        count = db.execute(query).fetchone()[0]
        return "Usuário existe." if count > 0 else "Usuário não encontrado."
    except Exception as e:
        return f"Erro: {e}"
