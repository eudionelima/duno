"""modules/csrf/logic.py"""
from core.database import get_db
from flask import session
from modules.csrf.source import low, medium, high, impossible


def run(level, user_id, new_email, submitted_token=None):
    db = get_db()
    if level == "low":    return low.handle(db, user_id, new_email)
    if level == "medium": return medium.handle(db, user_id, new_email)
    if level == "high":   return high.handle(db, user_id, new_email, submitted_token or "")
    return impossible.handle(db, user_id, new_email, submitted_token or "")
