"""modules/command_injection/source/medium.py — DUNO source view."""
import subprocess


_BLACKLIST = [";", "&&", "||", "`", "$", "|"]


def handle(cmd: str) -> str:
    """Medium: blacklist de separadores — bypassável com newline ou outras técnicas."""
    if not cmd:
        return ""
    for bad in _BLACKLIST:
        if bad in cmd:
            return "Caractere proibido detectado."
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
