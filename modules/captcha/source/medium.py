"""modules/captcha/source/medium.py — DUNO source view."""


def handle(db, challenge_id: int, answer: str) -> str:
    """Medium: valida server-side mas não marca como usado — reutilizável."""
    row = db.execute(
        "SELECT * FROM captcha_challenges WHERE id=?", (challenge_id,)
    ).fetchone()
    if not row:
        return "Desafio inválido."
    if row["answer"].strip().lower() == answer.strip().lower():
        return "CAPTCHA correto! (mas pode ser reutilizado)"
    return "CAPTCHA incorreto."
