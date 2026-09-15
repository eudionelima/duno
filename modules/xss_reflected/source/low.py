"""modules/xss_reflected/source/low.py — DUNO source view."""
from markupsafe import Markup


def handle(name: str) -> str:
    """Low: reflete input sem escape — XSS direto."""
    return Markup(f"<p>Olá, {name}!</p>")
