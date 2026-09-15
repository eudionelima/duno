"""modules/xss_dom/source/medium.py — DUNO source view."""
import re


def handle(name: str) -> str:
    """Medium: remove tags <script> — bypassável com <img onerror=...>."""
    cleaned = re.sub(r"<script.*?>.*?</script>", "", name, flags=re.IGNORECASE | re.DOTALL)
    return cleaned
