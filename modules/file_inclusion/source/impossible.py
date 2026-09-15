"""modules/file_inclusion/source/impossible.py — DUNO source view."""
import os


_ALLOWED = {"about.txt", "help.txt", "info.txt"}


def handle(page: str) -> str:
    """Impossible: whitelist + realpath para garantir que o arquivo está dentro do dir permitido."""
    if page not in _ALLOWED:
        return "Arquivo não permitido."
    base = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    )
    path = os.path.realpath(os.path.join(base, page))
    if not path.startswith(base + os.sep):
        return "Path traversal detectado."
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
