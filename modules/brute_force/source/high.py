"""modules/brute_force/source/high.py — DUNO source view."""
from werkzeug.security import check_password_hash
from flask import session


def handle(db, username: str, password: str, submitted_token: str) -> dict:
    """High: CSRF token obrigatório mas sem lockout — brute-force lento com extração de token ainda funciona."""
    expected = session.get("csrf_token_bf", "")
    if not expected or submitted_token != expected:
        return {"success": False, "msg": "Token CSRF inválido."}

    row = db.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    if row and check_password_hash(row["password_hash"], password):
        return {"success": True, "msg": f"Login bem-sucedido! Bem-vindo, {username}. (CSRF validado, sem lockout)"}
    return {"success": False, "msg": "Credenciais inválidas. (token CSRF validado, sem lockout)"}
