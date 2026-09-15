"""modules/weak_session/source/low.py — DUNO source view."""
import time


_counter = 0


def generate_session_id() -> str:
    """Low: ID sequencial — previsível, incremento de 1."""
    global _counter
    _counter += 1
    return str(_counter)
