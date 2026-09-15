"""modules/api_security/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("api_security", __name__)


@bp.route("/api_security", methods=["GET"])
@login_required
def index():
    level = get_level(session["user_id"], "api_security")
    result = None
    target_id = request.args.get("user_id", session.get("user_id", 1))
    try:
        target_id = int(target_id)
    except Exception:
        target_id = 1
    from modules.api_security.logic import run
    result = run(level, target_id)

    return render_template(
        "modules/api_security.html",
        level=level, result=result, target_id=target_id, module="api_security",
        current_level=level,
    )
