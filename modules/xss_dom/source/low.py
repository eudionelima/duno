"""modules/xss_dom/source/low.py — DUNO source view."""


def handle(name: str) -> str:
    """Low: parâmetro injetado no DOM via innerHTML sem sanitização."""
    # Server apenas ecoa — JS no template usa innerHTML
    return name
