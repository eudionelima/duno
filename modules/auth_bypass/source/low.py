"""modules/auth_bypass/source/low.py — DUNO source view."""


def check_access(user: dict) -> bool:
    """Low: verifica role somente via parâmetro GET — manipulável direto na URL."""
    return True  # sem verificação real
