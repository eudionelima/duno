"""modules/xss_dom/source/impossible.py — DUNO source view."""


def handle(name: str) -> str:
    """Impossible: server retorna dado — JS usa textContent (nunca innerHTML)."""
    # O template usa textContent, não innerHTML — XSS impossível via DOM
    return name
