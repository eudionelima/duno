"""modules/api_versioning/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("api_versioning", __name__)


@bp.route("/api_versioning", methods=["GET"])
@login_required
def index():
    level = get_level(session["user_id"], "api_versioning")
    result = None
    version = request.args.get("version", "v2")
    from modules.api_versioning.logic import run
    result = run(level, version)

    return render_template(
        "modules/api_versioning.html",
        level=level, result=result, version=version, module="api_versioning",
        current_level=level,
    )
