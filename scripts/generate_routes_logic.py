#!/usr/bin/env python3
"""generate_routes_logic.py — gera routes.py e logic.py para todos os módulos."""
import os

BASE = "/home/dione/Projects/duno"

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"[write] {path.replace(BASE+'/', '')}")

# ── Module definitions: (slug, title, icon, desc, route, special) ─────────────
MODULES = [
    ("command_injection", "Command Injection", "💻", "Injeção de comandos via entrada controlada", "/command_injection"),
    ("csrf",              "CSRF",              "🎭", "Requisição forjada entre sites",              "/csrf"),
    ("file_inclusion",    "File Inclusion",    "📂", "Inclusão de arquivos via parâmetro",          "/file_inclusion"),
    ("file_upload",       "File Upload",       "📤", "Upload inseguro de arquivos",                 "/file_upload"),
    ("captcha",           "Insecure CAPTCHA",  "🤖", "Bypass de mecanismo CAPTCHA",                "/captcha"),
    ("sqli",              "SQL Injection",      "🗄️",  "Manipulação de consultas SQL",               "/sqli"),
    ("sqli_blind",        "SQL Injection (Blind)", "👁️", "SQLi boolean-based e time-based",         "/sqli_blind"),
    ("weak_session",      "Weak Session IDs",  "🪪", "Sessões previsíveis ou manipuláveis",         "/weak_session"),
    ("xss_dom",           "XSS (DOM)",         "🌐", "Cross-Site Scripting via DOM",                "/xss_dom"),
    ("xss_reflected",     "XSS (Reflected)",   "↩️",  "XSS refletido por parâmetros",              "/xss_reflected"),
    ("xss_stored",        "XSS (Stored)",      "💾", "XSS persistido no guestbook",                 "/xss_stored"),
    ("csp_bypass",        "CSP Bypass",        "🛡️",  "Bypass de Content Security Policy",         "/csp_bypass"),
    ("js_attacks",        "JavaScript Attacks", "⚡", "Manipulação de valores client-side",         "/js_attacks"),
    ("auth_bypass",       "Authorisation Bypass","🚪","Acesso indevido a área administrativa",     "/auth_bypass"),
    ("open_redirect",     "Open HTTP Redirect", "↗️",  "Redirecionamento controlado pelo usuário",  "/open_redirect"),
    ("crypto",            "Cryptography",      "🔑", "Dados considerados protegidos",               "/crypto"),
    ("api_versioning",    "API Versioning",    "📡", "Acesso via versão de API obsoleta",            "/api_versioning"),
    ("mass_assignment",   "Mass Assignment",   "📋", "Manipulação de campos JSON",                   "/mass_assignment"),
    ("api_security",      "API Security",      "🔌", "Laboratório de segurança de API REST",         "/api_security"),
]

# ── Generic routes template ────────────────────────────────────────────────────
def make_routes(slug, title, route):
    special_imports = ""
    extra_logic = ""

    if slug == "command_injection":
        extra_logic = """
    cmd = ""
    result = None
    if request.method == "POST":
        cmd = request.form.get("cmd", "")
        from modules.command_injection.logic import run
        result = run(level, cmd)"""

    elif slug == "csrf":
        extra_logic = """
    import secrets as _sec
    csrf_token = _sec.token_hex(16)
    session["csrf_token_csrf"] = csrf_token
    result = None
    if request.method == "POST":
        from modules.csrf.logic import run
        new_email = request.form.get("new_email", "")
        submitted_token = request.form.get("csrf_token", "")
        result = run(level, session.get("user_id"), new_email, submitted_token)"""

    elif slug == "file_inclusion":
        extra_logic = """
    page = request.args.get("page", "")
    result = None
    _setup_pages()
    if page:
        from modules.file_inclusion.logic import run
        result = run(level, page)"""
        special_imports = "\nfrom modules.file_inclusion.logic import setup_pages as _setup_pages"

    elif slug == "file_upload":
        extra_logic = """
    result = None
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            result = "Nenhum arquivo selecionado."
        else:
            from modules.file_upload.logic import run
            result = run(level, request.files["file"])"""

    elif slug == "captcha":
        extra_logic = """
    from modules.captcha.logic import get_challenge, run
    challenge = get_challenge(level)
    result = None
    if request.method == "POST":
        challenge_id = request.form.get("challenge_id", "")
        answer = request.form.get("answer", "")
        result = run(level, challenge_id, answer)"""

    elif slug == "sqli":
        extra_logic = """
    rows = []
    result = None
    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        from modules.sqli.logic import run
        rows = run(level, user_id)"""

    elif slug == "sqli_blind":
        extra_logic = """
    result = None
    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        from modules.sqli_blind.logic import run
        result = run(level, user_id)"""

    elif slug == "weak_session":
        extra_logic = """
    from modules.weak_session.logic import generate_sid
    new_sid = generate_sid(level)"""

    elif slug in ("xss_dom", "xss_reflected"):
        extra_logic = f"""
    name = ""
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        from modules.{slug}.logic import run
        result = run(level, name)"""

    elif slug == "xss_stored":
        extra_logic = """
    from modules.xss_stored.logic import get_entries, save_entry
    if request.method == "POST":
        name = request.form.get("name", "")
        message = request.form.get("message", "")
        save_entry(level, name, message)
    entries = get_entries(level)"""

    elif slug == "csp_bypass":
        extra_logic = """
    from modules.csp_bypass.logic import get_csp, get_nonce
    nonce = get_nonce(level)
    name = ""
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        result = name
    csp_header = get_csp(level, nonce)"""

    elif slug == "js_attacks":
        extra_logic = """
    result = None
    if request.method == "POST":
        product_id = request.form.get("product_id", "1")
        price = request.form.get("price", "")
        from modules.js_attacks.logic import run
        result = run(level, product_id, price)"""

    elif slug == "auth_bypass":
        extra_logic = """
    from modules.auth_bypass.logic import check
    access = check(level)"""

    elif slug == "open_redirect":
        extra_logic = """
    url = request.args.get("url", "")
    redirect_result = None
    if url:
        from modules.open_redirect.logic import run
        redirect_result = run(level, url)
        if hasattr(redirect_result, "status_code"):
            return redirect_result"""

    elif slug == "crypto":
        extra_logic = """
    result = None
    if request.method == "POST":
        key = request.form.get("key", "flag")
        from modules.crypto.logic import run
        result = run(level, key)"""

    elif slug == "api_versioning":
        extra_logic = """
    result = None
    version = request.args.get("version", "v2")
    from modules.api_versioning.logic import run
    result = run(level, version)"""

    elif slug == "mass_assignment":
        extra_logic = """
    result = None
    if request.method == "POST":
        import json as _json
        try:
            data = _json.loads(request.form.get("payload", "{}"))
        except Exception:
            data = {}
        from modules.mass_assignment.logic import run
        result = run(level, session.get("user_id"), data)"""

    elif slug == "api_security":
        extra_logic = """
    result = None
    target_id = request.args.get("user_id", session.get("user_id", 1))
    try:
        target_id = int(target_id)
    except Exception:
        target_id = 1
    from modules.api_security.logic import run
    result = run(level, target_id)"""

    # Build render kwargs string
    kwargs_map = {
        "command_injection": "level=level, result=result, cmd=cmd, module=slug",
        "csrf": "level=level, result=result, csrf_token=csrf_token, module=slug",
        "file_inclusion": "level=level, result=result, page=page, module=slug",
        "file_upload": "level=level, result=result, module=slug",
        "captcha": "level=level, result=result, challenge=challenge, module=slug",
        "sqli": "level=level, rows=rows, module=slug",
        "sqli_blind": "level=level, result=result, module=slug",
        "weak_session": "level=level, new_sid=new_sid, module=slug",
        "xss_dom": "level=level, result=result, name=name, module=slug",
        "xss_reflected": "level=level, result=result, name=name, module=slug",
        "xss_stored": "level=level, entries=entries, module=slug",
        "csp_bypass": "level=level, result=result, name=name, nonce=nonce, csp_header=csp_header, module=slug",
        "js_attacks": "level=level, result=result, module=slug",
        "auth_bypass": "level=level, access=access, module=slug",
        "open_redirect": "level=level, module=slug",
        "crypto": "level=level, result=result, module=slug",
        "api_versioning": "level=level, result=result, version=version, module=slug",
        "mass_assignment": "level=level, result=result, module=slug",
        "api_security": "level=level, result=result, target_id=target_id, module=slug",
    }
    render_kwargs = kwargs_map.get(slug, "level=level, module=slug")
    render_kwargs = render_kwargs.replace("slug", f'"{slug}"')

    methods = '["GET", "POST"]'
    if slug in ("file_inclusion", "api_versioning", "api_security", "open_redirect"):
        methods = '["GET"]'

    return f'''"""modules/{slug}/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level
{special_imports}

bp = Blueprint("{slug}", __name__)


@bp.route("{route}", methods={methods})
@login_required
def index():
    level = get_level(session["user_id"], "{slug}")
    {extra_logic.strip()}

    return render_template(
        "modules/{slug}.html",
        {render_kwargs},
        current_level=level,
    )
'''


# ── Generic logic template ─────────────────────────────────────────────────────
def make_logic(slug):
    logics = {
"command_injection": '''"""modules/command_injection/logic.py"""
from modules.command_injection.source import low, medium, high, impossible


def run(level: str, cmd: str) -> str:
    if level == "low":      return low.handle(cmd)
    if level == "medium":   return medium.handle(cmd)
    if level == "high":     return high.handle(cmd)
    return impossible.handle(cmd)
''',

"csrf": '''"""modules/csrf/logic.py"""
from core.database import get_db
from flask import session
from modules.csrf.source import low, medium, high, impossible


def run(level, user_id, new_email, submitted_token=None):
    db = get_db()
    if level == "low":    return low.handle(db, user_id, new_email)
    if level == "medium": return medium.handle(db, user_id, new_email)
    if level == "high":   return high.handle(db, user_id, new_email, submitted_token or "")
    return impossible.handle(db, user_id, new_email, submitted_token or "")
''',

"file_inclusion": '''"""modules/file_inclusion/logic.py"""
import os
from modules.file_inclusion.source import low, medium, high, impossible


PAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "static", "pages")


def setup_pages():
    os.makedirs(PAGES_DIR, exist_ok=True)
    for name, content in [
        ("about.txt", "Sobre o DUNO — laboratório deliberadamente vulnerável."),
        ("help.txt", "Ajuda: use os módulos para aprender sobre vulnerabilidades web."),
        ("info.txt", "DUNO v1.0 — Python 3.11 / Flask 3.x / SQLite"),
    ]:
        path = os.path.join(PAGES_DIR, name)
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content)


def run(level: str, page: str) -> str:
    if level == "low":    return low.handle(page)
    if level == "medium": return medium.handle(page)
    if level == "high":   return high.handle(page)
    return impossible.handle(page)
''',

"file_upload": '''"""modules/file_upload/logic.py"""
from flask import current_app
from modules.file_upload.source import low, medium, high, impossible


def run(level: str, file) -> str:
    folder = current_app.config["UPLOAD_FOLDER"]
    if level == "low":    return low.handle(file, folder)
    if level == "medium": return medium.handle(file, folder)
    if level == "high":   return high.handle(file, folder)
    return impossible.handle(file, folder)
''',

"captcha": '''"""modules/captcha/logic.py"""
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
''',

"sqli": '''"""modules/sqli/logic.py"""
from core.database import get_db
from modules.sqli.source import low, medium, high, impossible


def run(level: str, user_id: str) -> list:
    db = get_db()
    if level == "low":    return low.handle(db, user_id)
    if level == "medium": return medium.handle(db, user_id)
    if level == "high":   return high.handle(db, user_id)
    return impossible.handle(db, user_id)
''',

"sqli_blind": '''"""modules/sqli_blind/logic.py"""
from core.database import get_db
from modules.sqli_blind.source import low, medium, high, impossible


def run(level: str, user_id: str) -> str:
    db = get_db()
    if level == "low":    return low.handle(db, user_id)
    if level == "medium": return medium.handle(db, user_id)
    if level == "high":   return high.handle(db, user_id)
    return impossible.handle(db, user_id)
''',

"weak_session": '''"""modules/weak_session/logic.py"""
from modules.weak_session.source import low, medium, high, impossible


def generate_sid(level: str) -> str:
    if level == "low":    return low.generate_session_id()
    if level == "medium": return medium.generate_session_id()
    if level == "high":   return high.generate_session_id()
    return impossible.generate_session_id()
''',

"xss_dom": '''"""modules/xss_dom/logic.py"""
from modules.xss_dom.source import low, medium, high, impossible


def run(level: str, name: str) -> str:
    if level == "low":    return low.handle(name)
    if level == "medium": return medium.handle(name)
    if level == "high":   return high.handle(name)
    return impossible.handle(name)
''',

"xss_reflected": '''"""modules/xss_reflected/logic.py"""
from modules.xss_reflected.source import low, medium, high, impossible


def run(level: str, name: str):
    if level == "low":    return low.handle(name)
    if level == "medium": return medium.handle(name)
    if level == "high":   return high.handle(name)
    return impossible.handle(name)
''',

"xss_stored": '''"""modules/xss_stored/logic.py"""
from core.database import get_db
from modules.xss_stored.source import low, medium, high, impossible


def save_entry(level: str, name: str, message: str):
    db = get_db()
    if level == "low":    return low.save_entry(db, name, message)
    if level == "medium": return medium.save_entry(db, name, message)
    if level == "high":   return high.save_entry(db, name, message)
    return impossible.save_entry(db, name, message)


def get_entries(level: str) -> list:
    db = get_db()
    if level == "low":    return low.get_entries(db)
    if level == "medium": return medium.get_entries(db)
    if level == "high":   return high.get_entries(db)
    return impossible.get_entries(db)
''',

"csp_bypass": '''"""modules/csp_bypass/logic.py"""
from modules.csp_bypass.source import low, medium, high, impossible


def get_nonce(level: str) -> str:
    if level == "impossible":
        return impossible.get_csp_nonce()
    return ""


def get_csp(level: str, nonce: str = "") -> str:
    if level == "low":    return low.get_csp_header()
    if level == "medium": return medium.get_csp_header()
    if level == "high":   return high.get_csp_header()
    return impossible.get_csp_header(nonce)
''',

"js_attacks": '''"""modules/js_attacks/logic.py"""
from modules.js_attacks.source import low, medium, high, impossible


def run(level: str, product_id: str, price: str) -> str:
    if level == "low":    return low.handle(price)
    if level == "medium": return medium.handle(price)
    if level == "high":   return high.handle(product_id, price)
    return impossible.handle(product_id)
''',

"auth_bypass": '''"""modules/auth_bypass/logic.py"""
from modules.auth_bypass.source import low, medium, high, impossible
from core.auth import current_user


def check(level: str) -> bool:
    user = current_user()
    if level == "low":    return low.check_access(user)
    if level == "medium": return medium.check_access(user)
    if level == "high":   return high.check_access(user)
    return impossible.check_access(user)
''',

"open_redirect": '''"""modules/open_redirect/logic.py"""
from modules.open_redirect.source import low, medium, high, impossible


def run(level: str, url: str):
    if level == "low":    return low.handle(url)
    if level == "medium": return medium.handle(url)
    if level == "high":   return high.handle(url)
    return impossible.handle(url)
''',

"crypto": '''"""modules/crypto/logic.py"""
from modules.crypto.source import low, medium, high, impossible


def run(level: str, key: str) -> str:
    if level == "low":    return low.handle(key)
    if level == "medium": return medium.handle(key)
    if level == "high":   return high.handle(key)
    return impossible.handle(key)
''',

"api_versioning": '''"""modules/api_versioning/logic.py"""
from modules.api_versioning.source import low, medium, high, impossible


def run(level: str, version: str) -> list:
    if level == "low":    return low.handle(version)
    if level == "medium": return medium.handle(version)
    if level == "high":   return high.handle(version)
    return impossible.handle()
''',

"mass_assignment": '''"""modules/mass_assignment/logic.py"""
from core.database import get_db
from modules.mass_assignment.source import low, medium, high, impossible


def run(level: str, user_id: int, data: dict) -> dict:
    db = get_db()
    if level == "low":    return low.handle(db, user_id, data)
    if level == "medium": return medium.handle(db, user_id, data)
    if level == "high":   return high.handle(db, user_id, data)
    return impossible.handle(db, user_id, data)
''',

"api_security": '''"""modules/api_security/logic.py"""
from modules.api_security.source import low, medium, high, impossible


def run(level: str, user_id: int) -> dict:
    if level == "low":    return low.get_user(user_id)
    if level == "medium": return medium.get_user(user_id)
    if level == "high":   return high.get_user(user_id)
    return impossible.get_user(user_id)
''',
    }
    return logics.get(slug, f'"""modules/{slug}/logic.py — placeholder"""\n')


# ── Write routes and logic ─────────────────────────────────────────────────────
for slug, title, icon, desc, route in MODULES:
    # __init__.py
    write(
        os.path.join(BASE, "modules", slug, "__init__.py"),
        f'"""modules/{slug}/__init__.py"""\nfrom modules.{slug}.routes import bp\n__all__ = ["bp"]\n',
    )
    # routes.py
    write(os.path.join(BASE, "modules", slug, "routes.py"), make_routes(slug, title, route))
    # logic.py
    write(os.path.join(BASE, "modules", slug, "logic.py"), make_logic(slug))

print("\n[done] Routes + logic gerados.")
