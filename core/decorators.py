"""core/decorators.py — T-012 decorators de proteção de rota."""
import functools
from flask import session, redirect, url_for, abort
from core.auth import current_user


def login_required(f):
    """Redireciona para /login se não autenticado."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Retorna 403 se não for admin."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        user = current_user()
        if user is None:
            return redirect(url_for("login"))
        if user.get("role") != "admin":
            abort(403)
        return f(*args, **kwargs)
    return decorated
