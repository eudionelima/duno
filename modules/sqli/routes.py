"""modules/sqli/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("sqli", __name__)


@bp.route("/sqli", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "sqli")
    rows = []
    result = None
    if request.method == "POST":
        user_id = request.form.get("user_id", "")
        from modules.sqli.logic import run
        rows = run(level, user_id)

    return render_template(
        "modules/sqli.html",
        level=level, rows=rows, module="sqli",
        current_level=level,
    )
