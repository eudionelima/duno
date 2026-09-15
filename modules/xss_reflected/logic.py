"""modules/xss_reflected/logic.py"""
from modules.xss_reflected.source import low, medium, high, impossible


def run(level: str, name: str):
    if level == "low":    return low.handle(name)
    if level == "medium": return medium.handle(name)
    if level == "high":   return high.handle(name)
    return impossible.handle(name)
