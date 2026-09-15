"""modules/csp_bypass/logic.py"""
from modules.csp_bypass.source import low, medium, high, impossible


def get_nonce(level: str) -> str:
    if level == "impossible":
        return impossible.get_csp_nonce()
    return ""


def get_csp(level: str, nonce: str = "") -> str:
    if level == "low":    return low.get_csp_header()
    if level == "medium": return medium.get_csp_header()
    if level == "high":   return high.get_csp_header()
    return impossible.get_csp_header(nonce)
