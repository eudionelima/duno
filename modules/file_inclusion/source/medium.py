"""modules/file_inclusion/source/medium.py — DUNO source view."""
import os


def handle(page: str) -> str:
    """Medium: bloqueia '../' — bypassável com encoding (%2e%2e%2f) ou duplo encoding."""
    if ".." in page or page.startswith("/"):
        return "Caminho inválido."
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
