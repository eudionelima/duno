"""modules/mass_assignment/source/medium.py — DUNO source view."""


def handle(db, user_id: int, data: dict) -> dict:
    """Medium: remove 'role' da lista — mas 'password_hash' ainda pode ser injetado."""
    data.pop("role", None)
    allowed = {"username"}
    fields = {k: v for k, v in data.items() if k in allowed or k == "password_hash"}
    if not fields:
        return {"error": "Sem campos para atualizar."}
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [user_id]
    db.execute(f"UPDATE users SET {set_clause} WHERE id=?", values)
    db.commit()
    return {"updated": list(fields.keys())}
