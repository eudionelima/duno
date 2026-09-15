"""core/reset.py — T-014 reset do laboratório."""
from core.database import get_db


def reset_lab():
    """
    Limpa tabelas de dados do laboratório e re-insere dados seed.
    Preserva: users, security_levels.
    Limpa: guestbook, secrets, api_tokens, captcha_challenges, audit_log, uploads lógicos.
    """
    db = get_db()

    db.execute("DELETE FROM guestbook")
    db.execute("DELETE FROM secrets")
    db.execute("DELETE FROM api_tokens")
    db.execute("DELETE FROM captcha_challenges")
    db.execute("DELETE FROM audit_log")

    # re-seed dados do laboratório
    _seed_lab_data(db)
    db.commit()


def _seed_lab_data(db):
    """Insere dados sintéticos de laboratório."""
    # secrets — usados por Cryptography e JS Attacks
    db.executemany(
        "INSERT INTO secrets (key, value) VALUES (?,?)",
        [
            ("flag", "DUNO{y0u_f0und_th3_s3cr3t}"),
            ("admin_password", "sup3r_s3cur3_p@ss"),
            ("api_key", "sk-duno-1234567890abcdef"),
        ],
    )

    # guestbook — dados iniciais para XSS Stored
    db.executemany(
        "INSERT INTO guestbook (name, message) VALUES (?,?)",
        [
            ("Alice", "Olá, este é o guestbook do DUNO!"),
            ("Bob", "Laboratório de segurança — bem-vindo."),
        ],
    )

    # api_tokens — para API Security lab
    db.executemany(
        "INSERT INTO api_tokens (user_id, token, version) VALUES (?,?,?)",
        [
            (1, "tok-admin-v1-legacy", "v1"),
            (2, "tok-user-v2-current", "v2"),
        ],
    )

    # captcha_challenges
    db.executemany(
        "INSERT INTO captcha_challenges (challenge, answer) VALUES (?,?)",
        [
            ("Quanto é 3 + 4?", "7"),
            ("Quanto é 5 + 2?", "7"),
            ("Quanto é 8 - 3?", "5"),
        ],
    )
