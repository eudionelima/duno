"""modules/open_redirect/source/low.py — DUNO source view."""
from flask import redirect as flask_redirect


def handle(url: str):
    """Low: redireciona para qualquer URL sem validação."""
    return flask_redirect(url)
