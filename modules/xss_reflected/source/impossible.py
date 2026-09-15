"""modules/xss_reflected/source/impossible.py — DUNO source view."""
from markupsafe import escape


def handle(name: str) -> str:
    """Impossible: escape completo via markupsafe — Jinja2 renderiza como texto."""
    return str(escape(name))
