"""modules/crypto/source/medium.py — DUNO source view."""
from core.database import get_db


def _xor(text: str, key: int = 42) -> bytes:
    return bytes(ord(c) ^ key for c in text)


def handle(key: str) -> str:
    """Medium: XOR com chave fixa — criptografia fraca."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    encrypted = _xor(row["value"]).hex()
    return f"Valor (XOR/42): {encrypted}"
