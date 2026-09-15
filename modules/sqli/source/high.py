"""modules/sqli/source/high.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """High: prepared statement mas o nível não valida tipo — ainda permite LIKE injection."""
    try:
        uid = int(user_id)
    except ValueError:
        return [{"error": "ID deve ser inteiro."}]
    rows = db.execute(
        "SELECT id, username, role FROM users WHERE id = ?", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
