"""modules/csp_bypass/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("csp_bypass", __name__)


@bp.route("/csp_bypass", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "csp_bypass")
    from modules.csp_bypass.logic import get_csp, get_nonce
    nonce = get_nonce(level)
    name = ""
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        result = name
    csp_header = get_csp(level, nonce)

    return render_template(
        "modules/csp_bypass.html",
        level=level, result=result, name=name, nonce=nonce, csp_header=csp_header, module="csp_bypass",
        current_level=level,
    )
