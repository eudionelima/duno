"""modules/xss_reflected/source/medium.py — DUNO source view."""
import re
from markupsafe import Markup


def handle(name: str) -> str:
    """Medium: remove <script> — bypassável com <ScRiPt> ou eventos."""
    cleaned = re.sub(r"<script>", "", name, flags=re.IGNORECASE)
    cleaned = re.sub(r"</script>", "", cleaned, flags=re.IGNORECASE)
    return Markup(f"<p>Olá, {cleaned}!</p>")
