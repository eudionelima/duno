"""modules/weak_session/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("weak_session", __name__)


@bp.route("/weak_session", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "weak_session")
    from modules.weak_session.logic import generate_sid
    new_sid = generate_sid(level)

    return render_template(
        "modules/weak_session.html",
        level=level, new_sid=new_sid, module="weak_session",
        current_level=level,
    )
