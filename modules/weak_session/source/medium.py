"""modules/weak_session/source/medium.py — DUNO source view."""
import time
import hashlib


def generate_session_id() -> str:
    """Medium: MD5 do timestamp — previsível se o atacante souber a hora."""
    ts = str(time.time())
    return hashlib.md5(ts.encode()).hexdigest()
