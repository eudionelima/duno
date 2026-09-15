"""modules/brute_force/source/low.py — DUNO source view."""
from werkzeug.security import check_password_hash


def handle(db, username: str, password: str) -> dict:
    """Low: sem qualquer proteção — compara hash sem rate limit, delay ou lockout."""
    row = db.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    if row and check_password_hash(row["password_hash"], password):
        return {"success": True, "msg": f"Login bem-sucedido! Bem-vindo, {username}."}
    return {"success": False, "msg": "Credenciais inválidas."}
