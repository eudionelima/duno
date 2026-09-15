"""modules/sqli/source/low.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """Low: concatenação direta — SQLi trivial: 1 OR 1=1--"""
    query = f"SELECT id, username, role FROM users WHERE id = {user_id}"
    try:
        rows = db.execute(query).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]
