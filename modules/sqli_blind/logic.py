"""modules/sqli_blind/logic.py"""
from core.database import get_db
from modules.sqli_blind.source import low, medium, high, impossible


def run(level: str, user_id: str) -> str:
    db = get_db()
    if level == "low":    return low.handle(db, user_id)
    if level == "medium": return medium.handle(db, user_id)
    if level == "high":   return high.handle(db, user_id)
    return impossible.handle(db, user_id)
