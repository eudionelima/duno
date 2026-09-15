"""modules/xss_stored/source/high.py — DUNO source view."""
import html
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """High: escapa na gravação — mas renderiza com Markup, revertendo o escape."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)",
               (html.escape(name), html.escape(message)))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
