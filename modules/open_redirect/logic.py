"""modules/open_redirect/logic.py"""
from modules.open_redirect.source import low, medium, high, impossible


def run(level: str, url: str):
    if level == "low":    return low.handle(url)
    if level == "medium": return medium.handle(url)
    if level == "high":   return high.handle(url)
    return impossible.handle(url)
