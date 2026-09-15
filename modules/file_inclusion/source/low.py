"""modules/file_inclusion/source/low.py — DUNO source view."""
import os


def handle(page: str) -> str:
    """Low: lê arquivo diretamente do parâmetro — LFI/RFI trivial."""
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
