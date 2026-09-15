"""modules/command_injection/source/impossible.py — DUNO source view."""
import subprocess
import shlex


_ALLOWED = {"ping", "nslookup", "host", "dig"}


def handle(cmd: str) -> str:
    """Impossible: lista branca de comandos + shlex.split sem shell=True."""
    if not cmd:
        return ""
    parts = shlex.split(cmd)
    if not parts or parts[0] not in _ALLOWED:
        return f"Comando não permitido. Permitidos: {', '.join(_ALLOWED)}"
    result = subprocess.run(parts, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
