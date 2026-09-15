"""modules/file_inclusion/source/high.py — DUNO source view."""
import os


_ALLOWED = {"about.txt", "help.txt", "info.txt"}


def handle(page: str) -> str:
    """High: whitelist de nomes mas sem validação de path completo — symlinks podem burlar."""
    if page not in _ALLOWED:
        return f"Arquivo não permitido. Permitidos: {', '.join(_ALLOWED)}"
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
