#!/usr/bin/env python3
"""
generate_modules.py — gera todos os arquivos de módulo DUNO com lógica real.
Executa uma vez e popula o projeto completo.
"""
import os

BASE = "/home/dione/Projects/duno"
MODS_DIR = os.path.join(BASE, "modules")
TMPL_DIR = os.path.join(BASE, "templates", "modules")

# ─── Helpers ──────────────────────────────────────────────────────────────────
def write(path, content, overwrite=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not overwrite and os.path.exists(path):
        return
    with open(path, "w") as f:
        f.write(content)
    print(f"[write] {path.replace(BASE+'/', '')}")

# ─── Source files — implementações reais ──────────────────────────────────────

SOURCES = {}

# ── command_injection ─────────────────────────────────────────────────────────
SOURCES["command_injection"] = {
"low": '''"""modules/command_injection/source/low.py — DUNO source view."""
import subprocess


def handle(cmd: str) -> str:
    """Low: executa input diretamente via shell=True — injeção trivial."""
    if not cmd:
        return ""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
''',
"medium": '''"""modules/command_injection/source/medium.py — DUNO source view."""
import subprocess


_BLACKLIST = [";", "&&", "||", "`", "$", "|"]


def handle(cmd: str) -> str:
    """Medium: blacklist de separadores — bypassável com newline ou outras técnicas."""
    if not cmd:
        return ""
    for bad in _BLACKLIST:
        if bad in cmd:
            return "Caractere proibido detectado."
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
''',
"high": '''"""modules/command_injection/source/high.py — DUNO source view."""
import subprocess
import re


def handle(cmd: str) -> str:
    """High: regex mais restritiva — permite só alnum, '.', '-', '_', espaço."""
    if not cmd:
        return ""
    if not re.match(r"^[\\w.\\-\\ ]+$", cmd):
        return "Entrada inválida."
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
''',
"impossible": '''"""modules/command_injection/source/impossible.py — DUNO source view."""
import subprocess
import shlex


_ALLOWED = {"ping", "nslookup", "host", "dig"}


def handle(cmd: str) -> str:
    """Impossible: lista branca de comandos + shlex.split sem shell=True."""
    if not cmd:
        return ""
    parts = shlex.split(cmd)
    if not parts or parts[0] not in _ALLOWED:
        return f"Comando não permitido. Permitidos: {', '.join(_ALLOWED)}"
    result = subprocess.run(parts, capture_output=True, text=True, timeout=5)
    return result.stdout + result.stderr
''',
}

# ── csrf ──────────────────────────────────────────────────────────────────────
SOURCES["csrf"] = {
"low": '''"""modules/csrf/source/low.py — DUNO source view."""


def handle(db, user_id: int, new_email: str) -> str:
    """Low: altera e-mail sem token CSRF — qualquer site pode forjar a requisição."""
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
''',
"medium": '''"""modules/csrf/source/medium.py — DUNO source view."""
from flask import request


def handle(db, user_id: int, new_email: str) -> str:
    """Medium: verifica Referer — bypassável com Referer forjado ou ausente."""
    ref = request.headers.get("Referer", "")
    if "localhost" not in ref and "127.0.0.1" not in ref:
        return "Referer inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
''',
"high": '''"""modules/csrf/source/high.py — DUNO source view."""
from flask import session


def handle(db, user_id: int, new_email: str, submitted_token: str) -> str:
    """High: token CSRF válido mas implementação tem falha — token fixo por sessão, não por form."""
    expected = session.get("csrf_token_csrf", "")
    if not expected or submitted_token != expected:
        return "Token CSRF inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
''',
"impossible": '''"""modules/csrf/source/impossible.py — DUNO source view."""
import secrets
import hashlib
from flask import session


def generate_token(user_id: int) -> str:
    """Gera token CSRF por (user, form, timestamp) — one-time use."""
    raw = f"{user_id}:{secrets.token_hex(16)}"
    session["csrf_token_impossible"] = raw
    return hashlib.sha256(raw.encode()).hexdigest()


def handle(db, user_id: int, new_email: str, submitted_token: str) -> str:
    """Impossible: token CSRF one-time + validação de senha atual."""
    stored = session.pop("csrf_token_impossible", None)
    if not stored:
        return "Token CSRF ausente ou expirado."
    expected = hashlib.sha256(stored.encode()).hexdigest()
    if submitted_token != expected:
        return "Token CSRF inválido."
    db.execute("UPDATE users SET username=? WHERE id=?", (new_email, user_id))
    db.commit()
    return f"E-mail alterado para: {new_email}"
''',
}

# ── file_inclusion ────────────────────────────────────────────────────────────
SOURCES["file_inclusion"] = {
"low": '''"""modules/file_inclusion/source/low.py — DUNO source view."""
import os


def handle(page: str) -> str:
    """Low: lê arquivo diretamente do parâmetro — LFI/RFI trivial."""
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
''',
"medium": '''"""modules/file_inclusion/source/medium.py — DUNO source view."""
import os


def handle(page: str) -> str:
    """Medium: bloqueia '../' — bypassável com encoding (%2e%2e%2f) ou duplo encoding."""
    if ".." in page or page.startswith("/"):
        return "Caminho inválido."
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
''',
"high": '''"""modules/file_inclusion/source/high.py — DUNO source view."""
import os


_ALLOWED = {"about.txt", "help.txt", "info.txt"}


def handle(page: str) -> str:
    """High: whitelist de nomes mas sem validação de path completo — symlinks podem burlar."""
    if page not in _ALLOWED:
        return f"Arquivo não permitido. Permitidos: {', '.join(_ALLOWED)}"
    base = os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    path = os.path.join(base, page)
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
''',
"impossible": '''"""modules/file_inclusion/source/impossible.py — DUNO source view."""
import os


_ALLOWED = {"about.txt", "help.txt", "info.txt"}


def handle(page: str) -> str:
    """Impossible: whitelist + realpath para garantir que o arquivo está dentro do dir permitido."""
    if page not in _ALLOWED:
        return "Arquivo não permitido."
    base = os.path.realpath(
        os.path.join(os.path.dirname(__file__), "..", "..", "..", "static", "pages")
    )
    path = os.path.realpath(os.path.join(base, page))
    if not path.startswith(base + os.sep):
        return "Path traversal detectado."
    try:
        with open(path) as f:
            return f.read()
    except Exception as e:
        return str(e)
''',
}

# ── file_upload ───────────────────────────────────────────────────────────────
SOURCES["file_upload"] = {
"low": '''"""modules/file_upload/source/low.py — DUNO source view."""
import os


def handle(file, upload_folder: str) -> str:
    """Low: salva qualquer arquivo sem verificação — upload de .php direto."""
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
''',
"medium": '''"""modules/file_upload/source/medium.py — DUNO source view."""
import os


_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif"}


def handle(file, upload_folder: str) -> str:
    """Medium: verifica Content-Type — bypassável via Burp alterando o header."""
    if file.content_type not in _ALLOWED_TYPES:
        return f"Tipo não permitido: {file.content_type}"
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
''',
"high": '''"""modules/file_upload/source/high.py — DUNO source view."""
import os


_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif"}


def handle(file, upload_folder: str) -> str:
    """High: verifica extensão e Content-Type — bypassável com double extension (shell.php.jpg)."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in _ALLOWED_EXT:
        return f"Extensão não permitida: {ext}"
    if not file.content_type.startswith("image/"):
        return f"Content-Type inválido: {file.content_type}"
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
''',
"impossible": '''"""modules/file_upload/source/impossible.py — DUNO source view."""
import os
import uuid
from PIL import Image
import io


def handle(file, upload_folder: str) -> str:
    """Impossible: valida magic bytes via PIL + renomeia com UUID + recomprime imagem."""
    try:
        data = file.read()
        img = Image.open(io.BytesIO(data))
        img.verify()  # raises se não for imagem válida
    except Exception:
        return "Arquivo não é uma imagem válida."

    file.seek(0)
    try:
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert("RGB")
    except Exception:
        return "Erro ao processar imagem."

    safe_name = uuid.uuid4().hex + ".jpg"
    path = os.path.join(upload_folder, safe_name)
    img.save(path, "JPEG", quality=85)
    return f"Imagem salva com segurança: {safe_name}"
''',
}

# ── captcha ───────────────────────────────────────────────────────────────────
SOURCES["captcha"] = {
"low": '''"""modules/captcha/source/low.py — DUNO source view."""


def handle(db, answer: str) -> str:
    """Low: valida CAPTCHA apenas no cliente (JS) — sem verificação server-side."""
    # servidor aceita qualquer valor
    return f"CAPTCHA aceito (sem verificação server-side): '{answer}'"
''',
"medium": '''"""modules/captcha/source/medium.py — DUNO source view."""


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
''',
"high": '''"""modules/captcha/source/high.py — DUNO source view."""


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
''',
"impossible": '''"""modules/captcha/source/impossible.py — DUNO source view."""
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
''',
}

# ── sqli ──────────────────────────────────────────────────────────────────────
SOURCES["sqli"] = {
"low": '''"""modules/sqli/source/low.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """Low: concatenação direta — SQLi trivial: 1 OR 1=1--"""
    query = f"SELECT id, username, role FROM users WHERE id = {user_id}"
    try:
        rows = db.execute(query).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]
''',
"medium": '''"""modules/sqli/source/medium.py — DUNO source view."""
import re


def handle(db, user_id: str) -> list:
    """Medium: remove palavras-chave SQL — bypassável com UNION/**/ ou case variation."""
    banned = ["or", "union", "select", "drop", "insert", "--", "#", "/*"]
    cleaned = user_id.lower()
    for b in banned:
        cleaned = cleaned.replace(b, "")
    query = f"SELECT id, username, role FROM users WHERE id = {cleaned}"
    try:
        rows = db.execute(query).fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]
''',
"high": '''"""modules/sqli/source/high.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """High: prepared statement mas o nível não valida tipo — ainda permite LIKE injection."""
    try:
        uid = int(user_id)
    except ValueError:
        return [{"error": "ID deve ser inteiro."}]
    rows = db.execute(
        "SELECT id, username, role FROM users WHERE id = ?", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
''',
"impossible": '''"""modules/sqli/source/impossible.py — DUNO source view."""


def handle(db, user_id: str) -> list:
    """Impossible: prepared statement + validação estrita de tipo + whitelisted columns."""
    try:
        uid = int(user_id)
        if uid <= 0:
            raise ValueError
    except ValueError:
        return [{"error": "ID deve ser inteiro positivo."}]
    rows = db.execute(
        "SELECT id, username, role FROM users WHERE id = ?", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
''',
}

# ── sqli_blind ────────────────────────────────────────────────────────────────
SOURCES["sqli_blind"] = {
"low": '''"""modules/sqli_blind/source/low.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Low: boolean-based blind — só retorna 'existe' ou 'não existe'."""
    query = f"SELECT COUNT(*) FROM users WHERE id = {user_id}"
    try:
        count = db.execute(query).fetchone()[0]
        return "Usuário existe." if count > 0 else "Usuário não encontrado."
    except Exception as e:
        return f"Erro: {e}"
''',
"medium": '''"""modules/sqli_blind/source/medium.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Medium: sanitiza aspas mas não previne injeção numérica."""
    user_id = user_id.replace("'", "").replace('"', "")
    query = f"SELECT COUNT(*) FROM users WHERE id = {user_id}"
    try:
        count = db.execute(query).fetchone()[0]
        return "Usuário existe." if count > 0 else "Usuário não encontrado."
    except Exception as e:
        return f"Erro: {e}"
''',
"high": '''"""modules/sqli_blind/source/high.py — DUNO source view."""
import time


def handle(db, user_id: str) -> str:
    """High: time-based — usa sqlite3 heavy query para inferir dados."""
    query = (
        f"SELECT CASE WHEN (SELECT COUNT(*) FROM users WHERE id={user_id})>0 "
        "THEN (SELECT COUNT(*) FROM sqlite_master) ELSE 0 END"
    )
    try:
        db.execute(query)
        return "Usuário existe."
    except Exception as e:
        return f"Erro: {e}"
''',
"impossible": '''"""modules/sqli_blind/source/impossible.py — DUNO source view."""


def handle(db, user_id: str) -> str:
    """Impossible: prepared statement + validação de tipo inteiro."""
    try:
        uid = int(user_id)
    except ValueError:
        return "ID inválido."
    count = db.execute(
        "SELECT COUNT(*) FROM users WHERE id=?", (uid,)
    ).fetchone()[0]
    return "Usuário existe." if count > 0 else "Usuário não encontrado."
''',
}

# ── weak_session ──────────────────────────────────────────────────────────────
SOURCES["weak_session"] = {
"low": '''"""modules/weak_session/source/low.py — DUNO source view."""
import time


_counter = 0


def generate_session_id() -> str:
    """Low: ID sequencial — previsível, incremento de 1."""
    global _counter
    _counter += 1
    return str(_counter)
''',
"medium": '''"""modules/weak_session/source/medium.py — DUNO source view."""
import time
import hashlib


def generate_session_id() -> str:
    """Medium: MD5 do timestamp — previsível se o atacante souber a hora."""
    ts = str(time.time())
    return hashlib.md5(ts.encode()).hexdigest()
''',
"high": '''"""modules/weak_session/source/high.py — DUNO source view."""
import time
import hashlib
import random


def generate_session_id() -> str:
    """High: MD5(timestamp + random) — entropia baixa se random não usar CSPRNG."""
    raw = str(time.time()) + str(random.random())
    return hashlib.sha1(raw.encode()).hexdigest()
''',
"impossible": '''"""modules/weak_session/source/impossible.py — DUNO source view."""
import secrets


def generate_session_id() -> str:
    """Impossible: 32 bytes de entropia criptográfica via secrets.token_hex."""
    return secrets.token_hex(32)
''',
}

# ── xss_dom ───────────────────────────────────────────────────────────────────
SOURCES["xss_dom"] = {
"low": '''"""modules/xss_dom/source/low.py — DUNO source view."""


def handle(name: str) -> str:
    """Low: parâmetro injetado no DOM via innerHTML sem sanitização."""
    # Server apenas ecoa — JS no template usa innerHTML
    return name
''',
"medium": '''"""modules/xss_dom/source/medium.py — DUNO source view."""
import re


def handle(name: str) -> str:
    """Medium: remove tags <script> — bypassável com <img onerror=...>."""
    cleaned = re.sub(r"<script.*?>.*?</script>", "", name, flags=re.IGNORECASE | re.DOTALL)
    return cleaned
''',
"high": '''"""modules/xss_dom/source/high.py — DUNO source view."""
import re


def handle(name: str) -> str:
    """High: remove várias tags — bypassável com SVG ou eventos HTML5."""
    cleaned = re.sub(r"<(script|iframe|object|embed|link)[^>]*>.*?</\\1>", "", name,
                     flags=re.IGNORECASE | re.DOTALL)
    cleaned = re.sub(r"on\\w+\\s*=", "", cleaned, flags=re.IGNORECASE)
    return cleaned
''',
"impossible": '''"""modules/xss_dom/source/impossible.py — DUNO source view."""


def handle(name: str) -> str:
    """Impossible: server retorna dado — JS usa textContent (nunca innerHTML)."""
    # O template usa textContent, não innerHTML — XSS impossível via DOM
    return name
''',
}

# ── xss_reflected ─────────────────────────────────────────────────────────────
SOURCES["xss_reflected"] = {
"low": '''"""modules/xss_reflected/source/low.py — DUNO source view."""
from markupsafe import Markup


def handle(name: str) -> str:
    """Low: reflete input sem escape — XSS direto."""
    return Markup(f"<p>Olá, {name}!</p>")
''',
"medium": '''"""modules/xss_reflected/source/medium.py — DUNO source view."""
import re
from markupsafe import Markup


def handle(name: str) -> str:
    """Medium: remove <script> — bypassável com <ScRiPt> ou eventos."""
    cleaned = re.sub(r"<script>", "", name, flags=re.IGNORECASE)
    cleaned = re.sub(r"</script>", "", cleaned, flags=re.IGNORECASE)
    return Markup(f"<p>Olá, {cleaned}!</p>")
''',
"high": '''"""modules/xss_reflected/source/high.py — DUNO source view."""
from markupsafe import escape, Markup


def handle(name: str) -> str:
    """High: escapa HTML mas usa Markup incorretamente — forçar Markup quebra o escape."""
    safe = escape(name)
    return Markup(f"<p>Olá, {safe}!</p>")
''',
"impossible": '''"""modules/xss_reflected/source/impossible.py — DUNO source view."""
from markupsafe import escape


def handle(name: str) -> str:
    """Impossible: escape completo via markupsafe — Jinja2 renderiza como texto."""
    return str(escape(name))
''',
}

# ── xss_stored ────────────────────────────────────────────────────────────────
SOURCES["xss_stored"] = {
"low": '''"""modules/xss_stored/source/low.py — DUNO source view."""
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """Low: salva sem escape — XSS persistido no guestbook."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (name, message))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
''',
"medium": '''"""modules/xss_stored/source/medium.py — DUNO source view."""
import re
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """Medium: remove <script> no momento de salvar — XSS com outros vetores."""
    clean_name = re.sub(r"<script.*?>.*?</script>", "", name, flags=re.IGNORECASE | re.DOTALL)
    clean_msg  = re.sub(r"<script.*?>.*?</script>", "", message, flags=re.IGNORECASE | re.DOTALL)
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (clean_name, clean_msg))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
''',
"high": '''"""modules/xss_stored/source/high.py — DUNO source view."""
import html
from markupsafe import Markup


def save_entry(db, name: str, message: str):
    """High: escapa na gravação — mas renderiza com Markup, revertendo o escape."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)",
               (html.escape(name), html.escape(message)))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": Markup(r["name"]), "message": Markup(r["message"])} for r in rows]
''',
"impossible": '''"""modules/xss_stored/source/impossible.py — DUNO source view."""
from markupsafe import escape


def save_entry(db, name: str, message: str):
    """Impossible: salva raw, escapa somente no template via Jinja2 autoescaping."""
    db.execute("INSERT INTO guestbook (name, message) VALUES (?,?)", (name, message))
    db.commit()


def get_entries(db) -> list:
    rows = db.execute("SELECT * FROM guestbook ORDER BY id DESC").fetchall()
    return [{"id": r["id"], "name": str(escape(r["name"])),
             "message": str(escape(r["message"]))} for r in rows]
''',
}

# ── csp_bypass ────────────────────────────────────────────────────────────────
SOURCES["csp_bypass"] = {
"low": '''"""modules/csp_bypass/source/low.py — DUNO source view."""


def get_csp_header() -> str:
    """Low: sem CSP — qualquer script externo carregável."""
    return ""


def handle(name: str) -> str:
    return name
''',
"medium": '''"""modules/csp_bypass/source/medium.py — DUNO source view."""


def get_csp_header() -> str:
    """Medium: CSP com 'unsafe-inline' — XSS inline ainda possível."""
    return "default-src 'self'; script-src 'self' 'unsafe-inline'"


def handle(name: str) -> str:
    return name
''',
"high": '''"""modules/csp_bypass/source/high.py — DUNO source view."""


def get_csp_header() -> str:
    """High: CSP com CDN confiável mas sem hash/nonce — JSONP bypass possível."""
    return "default-src 'self'; script-src 'self' https://cdnjs.cloudflare.com"


def handle(name: str) -> str:
    return name
''',
"impossible": '''"""modules/csp_bypass/source/impossible.py — DUNO source view."""
import secrets


def get_csp_nonce() -> str:
    return secrets.token_hex(16)


def get_csp_header(nonce: str) -> str:
    """Impossible: CSP com nonce por requisição + sem unsafe-inline + sem wildcards."""
    return (
        f"default-src 'none'; "
        f"script-src 'nonce-{nonce}'; "
        f"style-src 'self'; "
        f"img-src 'self' data:; "
        f"connect-src 'self'; "
        f"frame-ancestors 'none'"
    )


def handle(name: str) -> str:
    from markupsafe import escape
    return str(escape(name))
''',
}

# ── js_attacks ────────────────────────────────────────────────────────────────
SOURCES["js_attacks"] = {
"low": '''"""modules/js_attacks/source/low.py — DUNO source view."""


def handle(price: str) -> str:
    """Low: valor de preço validado somente no JS cliente — manipulável via DevTools."""
    try:
        p = float(price)
        return f"Compra realizada! Valor pago: R$ {p:.2f}"
    except ValueError:
        return "Valor inválido."
''',
"medium": '''"""modules/js_attacks/source/medium.py — DUNO source view."""


_MIN_PRICE = 99.90


def handle(price: str) -> str:
    """Medium: valida server-side mas compara float — manipulável com precisão."""
    try:
        p = float(price)
        if p < 0:
            return "Valor negativo não permitido."
        return f"Compra realizada! Valor pago: R$ {p:.2f}"
    except ValueError:
        return "Valor inválido."
''',
"high": '''"""modules/js_attacks/source/high.py — DUNO source view."""
from core.database import get_db


def handle(product_id: str, submitted_price: str) -> str:
    """High: verifica preço no banco — mas não valida autenticidade do product_id."""
    db = get_db()
    row = db.execute(
        "SELECT value FROM secrets WHERE key=?", (f"price_{product_id}",)
    ).fetchone()
    if not row:
        return "Produto não encontrado."
    expected = float(row["value"])
    submitted = float(submitted_price)
    if abs(submitted - expected) > 0.01:
        return f"Preço inválido. Esperado: R$ {expected:.2f}"
    return f"Compra realizada! Valor: R$ {submitted:.2f}"
''',
"impossible": '''"""modules/js_attacks/source/impossible.py — DUNO source view."""


_CATALOG = {
    "1": 99.90,
    "2": 199.90,
    "3": 49.90,
}


def handle(product_id: str) -> str:
    """Impossible: preço definido exclusivamente no servidor — cliente não envia valor."""
    price = _CATALOG.get(product_id)
    if price is None:
        return "Produto não encontrado."
    return f"Compra realizada! Valor: R$ {price:.2f}"
''',
}

# ── auth_bypass ───────────────────────────────────────────────────────────────
SOURCES["auth_bypass"] = {
"low": '''"""modules/auth_bypass/source/low.py — DUNO source view."""


def check_access(user: dict) -> bool:
    """Low: verifica role somente via parâmetro GET — manipulável direto na URL."""
    return True  # sem verificação real
''',
"medium": '''"""modules/auth_bypass/source/medium.py — DUNO source view."""
from flask import request


def check_access(user: dict) -> bool:
    """Medium: verifica cookie 'admin' — forjável com DevTools."""
    return request.cookies.get("admin") == "1"
''',
"high": '''"""modules/auth_bypass/source/high.py — DUNO source view."""
from flask import session


def check_access(user: dict) -> bool:
    """High: verifica sessão mas compara string — bypassável se sessão for manipulada."""
    return session.get("role") == "admin"
''',
"impossible": '''"""modules/auth_bypass/source/impossible.py — DUNO source view."""
from core.database import get_db
from flask import session


def check_access(user: dict) -> bool:
    """Impossible: verifica role diretamente no banco — sem confiar em sessão/cookie."""
    uid = session.get("user_id")
    if not uid:
        return False
    db = get_db()
    row = db.execute("SELECT role FROM users WHERE id=?", (uid,)).fetchone()
    return row is not None and row["role"] == "admin"
''',
}

# ── open_redirect ─────────────────────────────────────────────────────────────
SOURCES["open_redirect"] = {
"low": '''"""modules/open_redirect/source/low.py — DUNO source view."""
from flask import redirect as flask_redirect


def handle(url: str):
    """Low: redireciona para qualquer URL sem validação."""
    return flask_redirect(url)
''',
"medium": '''"""modules/open_redirect/source/medium.py — DUNO source view."""
from flask import redirect as flask_redirect


def handle(url: str):
    """Medium: bloqueia 'http://' mas não 'https://' — bypassável com https://evil.com."""
    if url.startswith("http://"):
        return "Redirecionamento externo não permitido."
    return flask_redirect(url)
''',
"high": '''"""modules/open_redirect/source/high.py — DUNO source view."""
from flask import redirect as flask_redirect
from urllib.parse import urlparse


def handle(url: str):
    """High: verifica host — bypassável com //evil.com ou subdomínio."""
    parsed = urlparse(url)
    if parsed.netloc and "localhost" not in parsed.netloc:
        return "Host externo não permitido."
    return flask_redirect(url)
''',
"impossible": '''"""modules/open_redirect/source/impossible.py — DUNO source view."""
from flask import redirect as flask_redirect, url_for


_ALLOWED = {"/", "/brute_force", "/sqli", "/xss_reflected"}


def handle(url: str):
    """Impossible: whitelist de URLs internas — redireciona para / se não estiver na lista."""
    if url not in _ALLOWED:
        return flask_redirect(url_for("index"))
    return flask_redirect(url)
''',
}

# ── crypto ────────────────────────────────────────────────────────────────────
SOURCES["crypto"] = {
"low": '''"""modules/crypto/source/low.py — DUNO source view."""
import base64
from core.database import get_db


def handle(key: str) -> str:
    """Low: dados codificados em base64 — não é criptografia."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    encoded = base64.b64encode(row["value"].encode()).decode()
    return f"Valor (base64): {encoded}"
''',
"medium": '''"""modules/crypto/source/medium.py — DUNO source view."""
from core.database import get_db


def _xor(text: str, key: int = 42) -> bytes:
    return bytes(ord(c) ^ key for c in text)


def handle(key: str) -> str:
    """Medium: XOR com chave fixa — criptografia fraca."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    encrypted = _xor(row["value"]).hex()
    return f"Valor (XOR/42): {encrypted}"
''',
"high": '''"""modules/crypto/source/high.py — DUNO source view."""
import hashlib
from core.database import get_db


def handle(key: str) -> str:
    """High: MD5 sem salt — vulnerável a rainbow tables."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    h = hashlib.md5(row["value"].encode()).hexdigest()
    return f"Hash MD5: {h}"
''',
"impossible": '''"""modules/crypto/source/impossible.py — DUNO source view."""
from werkzeug.security import generate_password_hash
from core.database import get_db


def handle(key: str) -> str:
    """Impossible: Werkzeug pbkdf2 com salt aleatório — não reversível."""
    db = get_db()
    row = db.execute("SELECT value FROM secrets WHERE key=?", (key,)).fetchone()
    if not row:
        return "Chave não encontrada."
    h = generate_password_hash(row["value"], method="pbkdf2:sha256", salt_length=16)
    return f"Hash seguro (pbkdf2:sha256): {h[:40]}…"
''',
}

# ── api_versioning ────────────────────────────────────────────────────────────
SOURCES["api_versioning"] = {
"low": '''"""modules/api_versioning/source/low.py — DUNO source view."""
from core.database import get_db


def handle(version: str) -> list:
    """Low: retorna todos os tokens de qualquer versão sem autenticação."""
    db = get_db()
    rows = db.execute("SELECT * FROM api_tokens").fetchall()
    return [dict(r) for r in rows]
''',
"medium": '''"""modules/api_versioning/source/medium.py — DUNO source view."""
from core.database import get_db


def handle(version: str) -> list:
    """Medium: filtra por versão mas v1 ainda acessível — dados legados expostos."""
    db = get_db()
    rows = db.execute(
        "SELECT * FROM api_tokens WHERE version=?", (version,)
    ).fetchall()
    return [dict(r) for r in rows]
''',
"high": '''"""modules/api_versioning/source/high.py — DUNO source view."""
from core.database import get_db
from flask import request


def handle(version: str) -> list:
    """High: exige header X-API-Version, mas v1 endpoint ainda existe."""
    header_ver = request.headers.get("X-API-Version", version)
    if header_ver == "v1":
        # v1 deprecated mas ainda funcional
        db = get_db()
        rows = db.execute("SELECT * FROM api_tokens WHERE version='v1'").fetchall()
        return [dict(r) for r in rows]
    db = get_db()
    rows = db.execute(
        "SELECT id, user_id, version FROM api_tokens WHERE version=?", (header_ver,)
    ).fetchall()
    return [dict(r) for r in rows]
''',
"impossible": '''"""modules/api_versioning/source/impossible.py — DUNO source view."""
from core.database import get_db
from flask import session


def handle() -> list:
    """Impossible: v1 desativado, filtra por user_id da sessão, sem campos sensíveis."""
    uid = session.get("user_id")
    db = get_db()
    rows = db.execute(
        "SELECT id, version FROM api_tokens WHERE user_id=? AND version='v2'", (uid,)
    ).fetchall()
    return [dict(r) for r in rows]
''',
}

# ── mass_assignment ───────────────────────────────────────────────────────────
SOURCES["mass_assignment"] = {
"low": '''"""modules/mass_assignment/source/low.py — DUNO source view."""
from core.database import get_db


def handle(db, user_id: int, data: dict) -> dict:
    """Low: atualiza qualquer campo recebido — permite elevar role para admin."""
    allowed_cols = {"username", "role"}
    fields = {k: v for k, v in data.items() if k in {"username", "role", "password_hash"}}
    if not fields:
        return {"error": "Sem campos para atualizar."}
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [user_id]
    db.execute(f"UPDATE users SET {set_clause} WHERE id=?", values)
    db.commit()
    return {"updated": fields}
''',
"medium": '''"""modules/mass_assignment/source/medium.py — DUNO source view."""


def handle(db, user_id: int, data: dict) -> dict:
    """Medium: remove 'role' da lista — mas 'password_hash' ainda pode ser injetado."""
    data.pop("role", None)
    allowed = {"username"}
    fields = {k: v for k, v in data.items() if k in allowed or k == "password_hash"}
    if not fields:
        return {"error": "Sem campos para atualizar."}
    set_clause = ", ".join(f"{k}=?" for k in fields)
    values = list(fields.values()) + [user_id]
    db.execute(f"UPDATE users SET {set_clause} WHERE id=?", values)
    db.commit()
    return {"updated": list(fields.keys())}
''',
"high": '''"""modules/mass_assignment/source/high.py — DUNO source view."""


def handle(db, user_id: int, data: dict) -> dict:
    """High: apenas 'username' permitido — mas sem validação de formato."""
    username = data.get("username", "")
    if not username:
        return {"error": "username é obrigatório."}
    db.execute("UPDATE users SET username=? WHERE id=?", (username, user_id))
    db.commit()
    return {"updated": {"username": username}}
''',
"impossible": '''"""modules/mass_assignment/source/impossible.py — DUNO source view."""
import re


def handle(db, user_id: int, data: dict) -> dict:
    """Impossible: whitelist estrita + validação de formato + sem campos internos."""
    username = data.get("username", "")
    if not username or not re.match(r"^[a-zA-Z0-9_]{3,32}$", username):
        return {"error": "username inválido (3–32 chars, alnum/underscore)."}
    db.execute("UPDATE users SET username=? WHERE id=?", (username, user_id))
    db.commit()
    return {"updated": {"username": username}}
''',
}

# ── api_security ──────────────────────────────────────────────────────────────
SOURCES["api_security"] = {
"low": '''"""modules/api_security/source/low.py — DUNO source view."""
from core.database import get_db


def get_user(user_id: int) -> dict:
    """Low: IDOR — sem verificação de propriedade. Acesse /api/users/<any_id>."""
    db = get_db()
    row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else {}
''',
"medium": '''"""modules/api_security/source/medium.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """Medium: verifica autenticação mas não ownership — IDOR autenticado."""
    uid = session.get("user_id")
    if not uid:
        return {"error": "Não autenticado."}
    db = get_db()
    row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
    return dict(row) if row else {}
''',
"high": '''"""modules/api_security/source/high.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """High: verifica ownership para users mas admin pode ver todos."""
    uid = session.get("user_id")
    if not uid:
        return {"error": "Não autenticado."}
    role = session.get("role")
    if role == "admin" or uid == user_id:
        db = get_db()
        row = db.execute("SELECT id, username, role FROM users WHERE id=?", (user_id,)).fetchone()
        return dict(row) if row else {}
    return {"error": "Acesso negado."}
''',
"impossible": '''"""modules/api_security/source/impossible.py — DUNO source view."""
from core.database import get_db
from flask import session


def get_user(user_id: int) -> dict:
    """Impossible: verifica ownership estritamente + rate limit implícito via audit_log."""
    uid = session.get("user_id")
    if not uid or uid != user_id:
        return {"error": "Acesso negado."}
    db = get_db()
    row = db.execute("SELECT id, username FROM users WHERE id=?", (uid,)).fetchone()
    return dict(row) if row else {}
''',
}

# ─── Write all source files ────────────────────────────────────────────────────
for mod, levels in SOURCES.items():
    for level, code in levels.items():
        path = os.path.join(MODS_DIR, mod, "source", f"{level}.py")
        write(path, code)

print("\n[done] Source files gerados.")
