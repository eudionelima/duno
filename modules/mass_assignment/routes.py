"""modules/mass_assignment/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("mass_assignment", __name__)


@bp.route("/mass_assignment", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "mass_assignment")
    result = None
    if request.method == "POST":
        import json as _json
        try:
            data = _json.loads(request.form.get("payload", "{}"))
        except Exception:
            data = {}
        from modules.mass_assignment.logic import run
        result = run(level, session.get("user_id"), data)

    return render_template(
        "modules/mass_assignment.html",
        level=level, result=result, module="mass_assignment",
        current_level=level,
    )
