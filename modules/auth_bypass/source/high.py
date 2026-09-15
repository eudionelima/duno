"""modules/auth_bypass/source/high.py — DUNO source view."""
from flask import session


def check_access(user: dict) -> bool:
    """High: verifica sessão mas compara string — bypassável se sessão for manipulada."""
    return session.get("role") == "admin"
