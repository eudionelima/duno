"""modules/captcha/logic.py"""
from core.database import get_db
from modules.captcha.source import low, medium, high, impossible


def get_challenge(level: str) -> dict:
    if level == "impossible":
        return impossible.generate_challenge()
    db = get_db()
    row = db.execute(
        "SELECT id, challenge FROM captcha_challenges WHERE used=0 LIMIT 1"
    ).fetchone()
    if not row:
        db.execute("UPDATE captcha_challenges SET used=0")
        db.commit()
        row = db.execute(
            "SELECT id, challenge FROM captcha_challenges LIMIT 1"
        ).fetchone()
    return {"id": row["id"], "question": row["challenge"]} if row else {"id": 0, "question": "?"}


def run(level: str, challenge_id, answer: str) -> str:
    db = get_db()
    if level == "low":    return low.handle(db, answer)
    if level == "medium": return medium.handle(db, int(challenge_id or 0), answer)
    if level == "high":   return high.handle(db, int(challenge_id or 0), answer)
    return impossible.handle(answer)
