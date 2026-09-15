"""modules/mass_assignment/logic.py"""
from core.database import get_db
from modules.mass_assignment.source import low, medium, high, impossible


def run(level: str, user_id: int, data: dict) -> dict:
    db = get_db()
    if level == "low":    return low.handle(db, user_id, data)
    if level == "medium": return medium.handle(db, user_id, data)
    if level == "high":   return high.handle(db, user_id, data)
    return impossible.handle(db, user_id, data)
