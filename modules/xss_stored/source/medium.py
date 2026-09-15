"""modules/xss_stored/source/medium.py — DUNO source view."""
import re
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """Medium: remove <script> no momento de salvar — XSS com outros vetores."""
    clean_name = re.sub(r"<script.*?>.*?</script>", "", name, flags=re.IGNORECASE | re.DOTALL)
    clean_msg  = re.sub(r"<script.*?>.*?</script>", "", message, flags=re.IGNORECASE | re.DOTALL)
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (clean_name, clean_msg))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
