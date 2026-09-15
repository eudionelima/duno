"""modules/file_inclusion/logic.py"""
import os
from modules.file_inclusion.source import low, medium, high, impossible


PAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "static", "pages")


def setup_pages():
    os.makedirs(PAGES_DIR, exist_ok=True)
    for name, content in [
        ("about.txt", "Sobre o DUNO — laboratório deliberadamente vulnerável."),
        ("help.txt", "Ajuda: use os módulos para aprender sobre vulnerabilidades web."),
        ("info.txt", "DUNO v1.0 — Python 3.11 / Flask 3.x / SQLite"),
    ]:
        path = os.path.join(PAGES_DIR, name)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)


def run(level: str, page: str) -> str:
    if level == "low":    return low.handle(page)
    if level == "medium": return medium.handle(page)
    if level == "high":   return high.handle(page)
    return impossible.handle(page)
