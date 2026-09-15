"""modules/xss_stored/source/impossible.py — DUNO source view."""
from markupsafe import escape


def save_entry(db, name: str, message: str):
    """Impossible: salva raw, escapa somente no template via Jinja2 autoescaping."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (name, message))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": str(escape(r["name"])),
             "message": str(escape(r["message"]))} for r in rows]
