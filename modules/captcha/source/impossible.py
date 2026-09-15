"""modules/captcha/source/impossible.py — DUNO source view."""
import secrets
import hashlib
from flask import session


def generate_challenge() -> dict:
    """Gera desafio matemático com token one-time."""
    a = secrets.randbelow(20) + 1
    b = secrets.randbelow(20) + 1
    answer = str(a + b)
    token = secrets.token_hex(16)
    h = hashlib.sha256(f"{answer}:{token}".encode()).hexdigest()
    session["captcha_hash"] = h
    session["captcha_token"] = token
    return {"question": f"Quanto é {a} + {b}?", "token": token}


def handle(answer: str) -> str:
    """Impossible: desafio server-side one-time com hash — impossível de contornar sem resolver."""
    token = session.pop("captcha_token", None)
    stored_hash = session.pop("captcha_hash", None)
    if not token or not stored_hash:
        return "Desafio expirado."
    h = hashlib.sha256(f"{answer.strip()}:{token}".encode()).hexdigest()
    if h == stored_hash:
        return "CAPTCHA correto! Ação permitida."
    return "CAPTCHA incorreto."
