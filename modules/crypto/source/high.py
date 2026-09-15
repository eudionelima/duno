"""modules/crypto/source/high.py — DUNO source view."""
import hashlib
from core.database import get_db


def handle(key: str) -> str:
    """High: MD5 sem salt — vulnerável a rainbow tables."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    h = hashlib.md5(row["value"].encode()).hexdigest()
    return f"Hash MD5: {h}"
