"""modules/crypto/logic.py"""
from modules.crypto.source import low, medium, high, impossible


def run(level: str, key: str) -> str:
    if level == "low":    return low.handle(key)
    if level == "medium": return medium.handle(key)
    if level == "high":   return high.handle(key)
    return impossible.handle(key)
