"""modules/brute_force/logic.py"""
from core.database import get_db
from modules.brute_force.source import low, medium, high, impossible


def run(level: str, username: str, password: str, csrf_token: str = "") -> dict:
    db = get_db()
    if level == "low":      return low.handle(db, username, password)
    if level == "medium":   return medium.handle(db, username, password)
    if level == "high":     return high.handle(db, username, password, csrf_token)
    return impossible.handle(db, username, password)
