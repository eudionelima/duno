"""modules/xss_dom/logic.py"""
from modules.xss_dom.source import low, medium, high, impossible


def run(level: str, name: str) -> str:
    if level == "low":    return low.handle(name)
    if level == "medium": return medium.handle(name)
    if level == "high":   return high.handle(name)
    return impossible.handle(name)
