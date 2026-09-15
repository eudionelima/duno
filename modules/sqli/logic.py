"""modules/sqli/logic.py"""
from core.database import get_db
from modules.sqli.source import low, medium, high, impossible


def run(level: str, user_id: str) -> list:
    db = get_db()
    if level == "low":    return low.handle(db, user_id)
    if level == "medium": return medium.handle(db, user_id)
    if level == "high":   return high.handle(db, user_id)
    return impossible.handle(db, user_id)
