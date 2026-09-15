"""modules/weak_session/source/impossible.py — DUNO source view."""
import secrets


def generate_session_id() -> str:
    """Impossible: 32 bytes de entropia criptográfica via secrets.token_hex."""
    return secrets.token_hex(32)
