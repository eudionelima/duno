"""modules/brute_force/source/medium.py — DUNO source view."""
import time
from werkzeug.security import check_password_hash


def handle(db, username: str, password: str) -> dict:
    """Medium: sleep de 2s após falha — mitiga velocidade, não força bruta real."""
    row = db.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    if row and check_password_hash(row["password_hash"], password):
        return {"success": True, "msg": f"Login bem-sucedido! Bem-vindo, {username}."}
    time.sleep(2)
    return {"success": False, "msg": "Credenciais inválidas. (delay de 2s aplicado)"}
