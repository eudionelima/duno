"""modules/auth_bypass/source/medium.py — DUNO source view."""
from flask import request


def check_access(user: dict) -> bool:
    """Medium: verifica cookie 'admin' — forjável com DevTools."""
    return request.cookies.get("admin") == "1"
