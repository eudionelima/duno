"""modules/api_versioning/source/high.py — DUNO source view."""
from core.database import get_db
from flask import request


def handle(version: str) -> list:
    """High: exige header X-API-Version, mas v1 endpoint ainda existe."""
    header_ver = request.headers.get("X-API-Version", version)
    if header_ver == "v1":
        # v1 deprecated mas ainda funcional
        db = get_db()
        rows = db.execute("SELECT * FROM api_tokens WHERE version='v1'").fetchall()
        return [dict(r) for r in rows]
    db = get_db()
    rows = db.execute(
        "SELECT id, user_id, version FROM api_tokens WHERE version=?", (header_ver,)
    ).fetchall()
    return [dict(r) for r in rows]
