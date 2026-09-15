"""modules/mass_assignment/source/low.py — DUNO source view."""
from core.database import get_db


def handle(db, user_id: int, data: dict) -> dict:
    """Low: atualiza qualquer campo recebido — permite elevar role para admin."""
    allowed_cols = {"username", "role"}
    fields = {k: v for k, v in data.items() if k in {"username", "role", "password_hash"}}
    if not fields:
        return {"error": "Sem campos para atualizar."}
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [user_id]
    db.execute(f"UPDATE users SET {set_clause} WHERE id=?", values)
    db.commit()
    return {"updated": fields}
