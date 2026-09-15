"""modules/open_redirect/source/impossible.py — DUNO source view."""
from flask import redirect as flask_redirect, url_for


_ALLOWED = {"/", "/brute_force", "/sqli", "/xss_reflected"}


def handle(url: str):
    """Impossible: whitelist de URLs internas — redireciona para / se não estiver na lista."""
    if url not in _ALLOWED:
        return flask_redirect(url_for("index"))
    return flask_redirect(url)
