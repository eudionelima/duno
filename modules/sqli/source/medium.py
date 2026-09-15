"""modules/sqli/source/medium.py — DUNO source view."""
import re


def handle(db, user_id: str) -> list:
    """Medium: remove palavras-chave SQL — bypassável com UNION/**/ ou case variation."""
    banned = ["or", "union", "select", "drop", "insert", "--", "#", "/*"]
    cleaned = user_id.lower()
    for b in banned:
        cleaned = cleaned.replace(b, "")
    query = f"SELECT id, username, role FROM users WHERE id = {cleaned}"
    try:
        rows = db.execute(query).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]
