"""modules/crypto/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("crypto", __name__)


@bp.route("/crypto", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "crypto")
    result = None
    if request.method == "POST":
        key = request.form.get("key", "flag")
        from modules.crypto.logic import run
        result = run(level, key)

    return render_template(
        "modules/crypto.html",
        level=level, result=result, module="crypto",
        current_level=level,
    )
