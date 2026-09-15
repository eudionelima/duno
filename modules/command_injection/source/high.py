"""modules/command_injection/source/high.py — DUNO source view."""
import subprocess
import re


def handle(cmd: str) -> str:
    """High: regex mais restritiva — permite só alnum, '.', '-', '_', espaço."""
    if not cmd:
        return ""
    if not re.match(r"^[\w.\-\ ]+$", cmd):
        return "Entrada inválida."
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
