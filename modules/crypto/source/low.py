"""modules/crypto/source/low.py — DUNO source view."""
import base64
from core.database import get_db


def handle(key: str) -> str:
    """Low: dados codificados em base64 — não é criptografia."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    encoded = base64.b64encode(row["value"].encode()).decode()
    return f"Valor (base64): {encoded}"
