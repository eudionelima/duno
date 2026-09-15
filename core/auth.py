"""core/auth.py — T-012 autenticação via sessão Flask."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from core.database import get_db


def login_user(username: str, password: str):
    """
    Valida credenciais. Retorna dict do usuário ou None.
    Versão low: sem rate limit, sem brute-force protection.
    """
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE username=?", (username,)
    ).fetchone()
    if user and check_password_hash(user["password_hash"], password):
        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        return dict(user)
    return None


def logout_user():
    session.clear()


def current_user():
    """Retorna dict do usuário logado ou None."""
    uid = session.get("user_id")
    if uid is None:
        return None
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    return dict(row) if row else None


def hash_password(password: str) -> str:
    return generate_password_hash(password)
