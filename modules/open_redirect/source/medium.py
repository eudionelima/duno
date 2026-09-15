"""modules/open_redirect/source/medium.py — DUNO source view."""
from flask import redirect as flask_redirect


def handle(url: str):
    """Medium: bloqueia 'http://' mas não 'https://' — bypassável com https://evil.com."""
    if url.startswith("http://"):
        return "Redirecionamento externo não permitido."
    return flask_redirect(url)
