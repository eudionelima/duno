"""modules/captcha/source/high.py — DUNO source view."""


def handle(db, challenge_id: int, answer: str) -> str:
    """High: marca como usado, mas exige somente correspondência de texto — trivialmente reversível."""
    row = db.execute(
        "SELECT * FROM captcha_challenges WHERE id=? AND used=0", (challenge_id,)
    ).fetchone()
    if not row:
        return "Desafio inválido ou já usado."
    if row["answer"].strip().lower() == answer.strip().lower():
        db.execute("UPDATE captcha_challenges SET used=1 WHERE id=?", (challenge_id,))
        db.commit()
        return "CAPTCHA correto!"
    return "CAPTCHA incorreto."
