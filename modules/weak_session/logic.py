"""modules/weak_session/logic.py"""
from modules.weak_session.source import low, medium, high, impossible


def generate_sid(level: str) -> str:
    if level == "low":    return low.generate_session_id()
    if level == "medium": return medium.generate_session_id()
    if level == "high":   return high.generate_session_id()
    return impossible.generate_session_id()
