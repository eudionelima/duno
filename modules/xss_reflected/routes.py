"""modules/xss_reflected/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("xss_reflected", __name__)


@bp.route("/xss_reflected", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "xss_reflected")
    name = ""
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        from modules.xss_reflected.logic import run
        result = run(level, name)

    return render_template(
        "modules/xss_reflected.html",
        level=level, result=result, name=name, module="xss_reflected",
        current_level=level,
    )
