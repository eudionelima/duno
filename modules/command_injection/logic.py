"""modules/command_injection/logic.py"""
from modules.command_injection.source import low, medium, high, impossible


def run(level: str, cmd: str) -> str:
    if level == "low":      return low.handle(cmd)
    if level == "medium":   return medium.handle(cmd)
    if level == "high":     return high.handle(cmd)
    return impossible.handle(cmd)


