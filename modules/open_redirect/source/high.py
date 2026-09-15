"""modules/open_redirect/source/high.py — DUNO source view."""
from flask import redirect as flask_redirect
from urllib.parse import urlparse


def handle(url: str):
    """High: verifica host — bypassável com //evil.com ou subdomínio."""
    parsed = urlparse(url)
    if parsed.netloc and "localhost" not in parsed.netloc:
        return "Host externo não permitido."
    return flask_redirect(url)
