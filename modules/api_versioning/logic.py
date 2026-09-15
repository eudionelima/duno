"""modules/api_versioning/logic.py"""
from modules.api_versioning.source import low, medium, high, impossible


def run(level: str, version: str) -> list:
    if level == "low":    return low.handle(version)
    if level == "medium": return medium.handle(version)
    if level == "high":   return high.handle(version)
    return impossible.handle()
