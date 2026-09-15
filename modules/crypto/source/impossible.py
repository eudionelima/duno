"""modules/crypto/source/impossible.py — DUNO source view."""
from werkzeug.security import generate_password_hash
from core.database import get_db


def handle(key: str) -> str:
    """Impossible: Werkzeug pbkdf2 com salt aleatório — não reversível."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    h = generate_password_hash(row["value"], method="pbkdf2:sha256", salt_length=16)
    return f"Hash seguro (pbkdf2:sha256): {h[:40]}…"
