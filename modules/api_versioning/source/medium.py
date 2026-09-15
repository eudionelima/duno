"""modules/api_versioning/source/medium.py — DUNO source view."""
from core.database import get_db


def handle(version: str) -> list:
    """Medium: filtra por versão mas v1 ainda acessível — dados legados expostos."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM api_tokens WHERE version=?", (version,)
    ).fetchall()
    return [dict(r) for r in rows]
