"""modules/js_attacks/logic.py"""
from modules.js_attacks.source import low, medium, high, impossible


def run(level: str, product_id: str, price: str) -> str:
    if level == "low":    return low.handle(price)
    if level == "medium": return medium.handle(price)
    if level == "high":   return high.handle(product_id, price)
    return impossible.handle(product_id)
