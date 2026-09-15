"""modules/csrf/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("csrf", __name__)


@bp.route("/csrf", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "csrf")
    import secrets as _sec
    csrf_token = _sec.token_hex(16)
    session["csrf_token_csrf"] = csrf_token
    result = None
    if request.method == "POST":
        from modules.csrf.logic import run
        new_email = request.form.get("new_email", "")
        submitted_token = request.form.get("csrf_token", "")
        result = run(level, session.get("user_id"), new_email, submitted_token)

    return render_template(
        "modules/csrf.html",
        level=level, result=result, csrf_token=csrf_token, module="csrf",
        current_level=level,
    )
