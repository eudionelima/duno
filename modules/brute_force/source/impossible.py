"""modules/brute_force/source/impossible.py — DUNO source view."""
from werkzeug.security import check_password_hash
from flask import request
from core.database import get_db


def handle(db, username: str, password: str) -> dict:
    """Impossible: lockout após 3 falhas em 15min por IP + audit log."""
    recent_fails = db.execute(
        "SELECT COUNT(*) FROM audit_log WHERE action='brute_fail' AND ip=? "
        "AND ts > datetime('now','-15 minutes')",
        (request.remote_addr,),
    ).fetchone()[0]

    if recent_fails >= 3:
        return {"success": False, "msg": "Conta bloqueada por 15 minutos após múltiplas falhas."}

    row = db.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()

    if row and check_password_hash(row["password_hash"], password):
        db.execute(
            "INSERT INTO audit_log (user_id, action, ip) VALUES (?,?,?)",
            (row["id"], "login_ok", request.remote_addr),
        )
        db.commit()
        return {"success": True, "msg": f"Login bem-sucedido! Falha registrada: 0/{3}. Bem-vindo, {username}."}

    db.execute(
        "INSERT INTO audit_log (user_id, action, ip) VALUES (?,?,?)",
        (None, "brute_fail", request.remote_addr),
    )
    db.commit()
    fails = recent_fails + 1
    return {"success": False, "msg": f"Credenciais inválidas. Falhas: {fails}/{3}. Próximas bloqueiam por 15min."}
