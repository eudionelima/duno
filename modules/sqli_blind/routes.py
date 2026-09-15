"""modules/sqli_blind/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("sqli_blind", __name__)


@bp.route("/sqli_blind", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "sqli_blind")
    result = None
    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        from modules.sqli_blind.logic import run
        result = run(level, user_id)

    return render_template(
        "modules/sqli_blind.html",
        level=level, result=result, module="sqli_blind",
        current_level=level,
    )
