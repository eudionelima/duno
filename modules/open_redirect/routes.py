"""modules/open_redirect/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("open_redirect", __name__)


@bp.route("/open_redirect", methods=["GET"])
@login_required
def index():
    level = get_level(session["user_id"], "open_redirect")
    url = request.args.get("url", "")
    redirect_result = None
    if url:
        from modules.open_redirect.logic import run
        redirect_result = run(level, url)
        if hasattr(redirect_result, "status_code"):
            return redirect_result

    return render_template(
        "modules/open_redirect.html",
        level=level, module="open_redirect",
        current_level=level,
    )
