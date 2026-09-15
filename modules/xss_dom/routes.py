"""modules/xss_dom/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("xss_dom", __name__)


@bp.route("/xss_dom", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "xss_dom")
    name = ""
    result = None
    if request.method == "POST":
        name = request.form.get("name", "")
        from modules.xss_dom.logic import run
        result = run(level, name)

    return render_template(
        "modules/xss_dom.html",
        level=level, result=result, name=name, module="xss_dom",
        current_level=level,
    )
