"""modules/weak_session/source/high.py — DUNO source view."""
import time
import hashlib
import random


def generate_session_id() -> str:
    """High: MD5(timestamp + random) — entropia baixa se random não usar CSPRNG."""
    raw = str(time.time()) + str(random.random())
    return hashlib.sha1(raw.encode()).hexdigest()
