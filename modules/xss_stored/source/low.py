"""modules/xss_stored/source/low.py — DUNO source view."""
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """Low: salva sem escape — XSS persistido no guestbook."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (name, message))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
