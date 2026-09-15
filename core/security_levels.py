"""core/security_levels.py — T-011 persistência de nível por (user, module)."""
from core.database import get_db

VALID_LEVELS = ("low", "medium", "high", "impossible")
VALID_MODULES = (
    "brute_force", "command_injection", "csrf", "file_inclusion",
    "file_upload", "captcha", "sqli", "sqli_blind", "weak_session",
    "xss_dom", "xss_reflected", "xss_stored", "csp_bypass", "js_attacks",
    "auth_bypass", "open_redirect", "crypto", "api_versioning",
    "mass_assignment", "api_security",
)


def get_level(user_id: int, module: str) -> str:
    """Retorna o nível atual do módulo para o usuário; padrão 'low'."""
    db = get_db()
    row = db.execute(
        "SELECT level FROM security_levels WHERE user_id=? AND module=?",
        (user_id, module),
    ).fetchone()
    return row["level"] if row else "low"


def set_level(user_id: int, module: str, level: str) -> bool:
    """Persiste o nível. Retorna False se inválido."""
    if level not in VALID_LEVELS:
        return False
    db = get_db()
    db.execute(
        """INSERT INTO security_levels (user_id, module, level)
           VALUES (?, ?, ?)
           ON CONFLICT(user_id, module) DO UPDATE SET level=excluded.level""",
        (user_id, module, level),
    )
    db.commit()
    return True
