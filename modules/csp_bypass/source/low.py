"""modules/csp_bypass/source/low.py — DUNO source view."""


def get_csp_header() -> str:
    """Low: sem CSP — qualquer script externo carregável."""
    return ""


def handle(name: str) -> str:
    return name
