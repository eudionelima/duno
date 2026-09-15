"""modules/xss_reflected/source/high.py — DUNO source view."""
from markupsafe import escape, Markup


def handle(name: str) -> str:
    """High: escapa HTML mas usa Markup incorretamente — forçar Markup quebra o escape."""
    safe = escape(name)
    return Markup(f"<p>Olá, {safe}!</p>")
