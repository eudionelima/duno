"""modules/captcha/source/low.py — DUNO source view."""


def handle(db, answer: str) -> str:
    """Low: valida CAPTCHA apenas no cliente (JS) — sem verificação server-side."""
    # servidor aceita qualquer valor
    return f"CAPTCHA aceito (sem verificação server-side): '{answer}'"
