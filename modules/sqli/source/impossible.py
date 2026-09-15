"""modules/sqli/source/impossible.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """Impossible: prepared statement + validação estrita de tipo + whitelisted columns."""
    try:
        uid = int(user_id)
        if uid <= 0:
            raise ValueError
    except ValueError:
        return [{"error": "ID deve ser inteiro positivo."}]
    rows = db.execute(
        "SELECT id, username, role FROM users WHERE id = ?", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
