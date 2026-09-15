"""modules/api_security/logic.py"""
from modules.api_security.source import low, medium, high, impossible


def run(level: str, user_id: int) -> dict:
    if level == "low":    return low.get_user(user_id)
    if level == "medium": return medium.get_user(user_id)
    if level == "high":   return high.get_user(user_id)
    return impossible.get_user(user_id)
