"""modules/xss_stored/logic.py"""
from core.database import get_db
from modules.xss_stored.source import low, medium, high, impossible


def save_entry(level: str, name: str, message: str):
    db = get_db()
    if level == "low":    return low.save_entry(db, name, message)
    if level == "medium": return medium.save_entry(db, name, message)
    if level == "high":   return high.save_entry(db, name, message)
    return impossible.save_entry(db, name, message)


def get_entries(level: str) -> list:
    db = get_db()
    if level == "low":    return low.get_entries(db)
    if level == "medium": return medium.get_entries(db)
    if level == "high":   return high.get_entries(db)
    return impossible.get_entries(db)
