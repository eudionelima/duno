"""modules/xss_dom/source/high.py — DUNO source view."""
import re


def handle(name: str) -> str:
    """High: remove várias tags — bypassável com SVG ou eventos HTML5."""
    cleaned = re.sub(r"<(script|iframe|object|embed|link)[^>]*>.*?</\1>", "", name,
                     flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"on\w+\s*=", "", cleaned, flags=re.IGNORECASE)
    return cleaned
