"""modules/csp_bypass/source/impossible.py — DUNO source view."""
import secrets


def get_csp_nonce() -> str:
    return secrets.token_hex(16)


def get_csp_header(nonce: str) -> str:
    """Impossible: CSP com nonce por requisição + sem unsafe-inline + sem wildcards."""
    return (
        f"default-src 'none'; "
        f"script-src 'nonce-{nonce}'; "
        f"style-src 'self'; "
        f"img-src 'self' data:; "
        f"connect-src 'self'; "
        f"frame-ancestors 'none'"
    )


def handle(name: str) -> str:
    from markupsafe import escape
    return str(escape(name))
