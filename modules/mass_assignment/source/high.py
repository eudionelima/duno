"""modules/mass_assignment/source/high.py — DUNO source view."""


def handle(db, user_id: int, data: dict) -> dict:
    """High: apenas 'username' permitido — mas sem validação de formato."""
    username = data.get("username", "")
    if not username:
        return {"error": "username é obrigatório."}
    db.execute("UPDATE users SET username=? WHERE id=?", (username, user_id))
    db.commit()
    return {"updated": {"username": username}}
