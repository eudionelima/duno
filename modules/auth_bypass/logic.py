"""modules/auth_bypass/logic.py"""
from modules.auth_bypass.source import low, medium, high, impossible
from core.auth import current_user


def check(level: str) -> bool:
    user = current_user()
    if level == "low":    return low.check_access(user)
    if level == "medium": return medium.check_access(user)
    if level == "high":   return high.check_access(user)
    return impossible.check_access(user)
