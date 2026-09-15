"""modules/auth_bypass/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("auth_bypass", __name__)


@bp.route("/auth_bypass", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "auth_bypass")
    from modules.auth_bypass.logic import check
    access = check(level)

    return render_template(
        "modules/auth_bypass.html",
        level=level, access=access, module="auth_bypass",
        current_level=level,
    )
