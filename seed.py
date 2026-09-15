"""seed.py — T-010 criação e seed inicial do banco DUNO."""
import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.environ.get("DATABASE", "/app/data/duno.db")

DDL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS security_levels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    module TEXT NOT NULL,
    level TEXT NOT NULL CHECK(level IN ('low','medium','high','impossible')),
    UNIQUE(user_id, module),
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS guestbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS secrets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT,
    value TEXT
);

CREATE TABLE IF NOT EXISTS api_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    token TEXT,
    version TEXT
);

CREATE TABLE IF NOT EXISTS captcha_challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge TEXT,
    answer TEXT,
    used INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT,
    ip TEXT,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def seed():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(DDL)

    # Idempotente: só insere se users estiver vazio
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count == 0:
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
            ("admin", generate_password_hash("password"), "admin"),
        )
        conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
            ("user", generate_password_hash("password"), "user"),
        )
        conn.commit()
        print("[seed] Usuários criados: admin/password, user/password")
    else:
        print("[seed] Usuários já existem — pulando inserção.")

    # Lab data idempotente
    if conn.execute("SELECT COUNT(*) FROM secrets").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO secrets (key, value) VALUES (?,?)",
            [
                ("flag", "DUNO{y0u_f0und_th3_s3cr3t}"),
                ("admin_password", "sup3r_s3cur3_p@ss"),
                ("api_key", "sk-duno-1234567890abcdef"),
            ],
        )
        conn.commit()

    if conn.execute("SELECT COUNT(*) FROM guestbook").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO guestbook (name, message) VALUES (?,?)",
            [
                ("Alice", "Olá, este é o guestbook do DUNO!"),
                ("Bob", "Laboratório de segurança — bem-vindo."),
            ],
        )
        conn.commit()

    if conn.execute("SELECT COUNT(*) FROM api_tokens").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO api_tokens (user_id, token, version) VALUES (?,?,?)",
            [
                (1, "tok-admin-v1-legacy", "v1"),
                (2, "tok-user-v2-current", "v2"),
            ],
        )
        conn.commit()

    if conn.execute("SELECT COUNT(*) FROM captcha_challenges").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO captcha_challenges (challenge, answer) VALUES (?,?)",
            [
                ("Quanto é 3 + 4?", "7"),
                ("Quanto é 5 + 2?", "7"),
                ("Quanto é 8 - 3?", "5"),
            ],
        )
        conn.commit()

    conn.close()
    print(f"[seed] Banco OK: {DB_PATH}")


if __name__ == "__main__":
    seed()
