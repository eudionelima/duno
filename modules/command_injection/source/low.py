"""modules/command_injection/source/low.py — DUNO source view."""
import subprocess


def handle(cmd: str) -> str:
    """Low: executa input diretamente via shell=True — injeção trivial."""
    if not cmd:
        return ""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
