"""modules/mass_assignment/source/impossible.py — DUNO source view."""
import re


def handle(db, user_id: int, data: dict) -> dict:
    """Impossible: whitelist estrita + validação de formato + sem campos internos."""
    username = data.get("username", "")
    if not username or not re.match(r"^[a-zA-Z0-9_]{3,32}$", username):
        return {"error": "username inválido (3–32 chars, alnum/underscore)."}
    db.execute("UPDATE users SET username=? WHERE id=?", (username, user_id))
    db.commit()
    return {"updated": {"username": username}}
