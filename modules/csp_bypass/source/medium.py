"""modules/csp_bypass/source/medium.py — DUNO source view."""


def get_csp_header() -> str:
    """Medium: CSP com 'unsafe-inline' — XSS inline ainda possível."""
    return "default-src 'self'; script-src 'self' 'unsafe-inline'"


def handle(name: str) -> str:
    return name
