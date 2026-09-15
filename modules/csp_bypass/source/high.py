"""modules/csp_bypass/source/high.py — DUNO source view."""


def get_csp_header() -> str:
    """High: CSP com CDN confiável mas sem hash/nonce — JSONP bypass possível."""
    return "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com"


def handle(name: str) -> str:
    return name
