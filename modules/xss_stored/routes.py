"""modules/xss_stored/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("xss_stored", __name__)


@bp.route("/xss_stored", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "xss_stored")
    from modules.xss_stored.logic import get_entries, save_entry
    if request.method == "POST":
        name = request.form.get("name", "")
        message = request.form.get("message", "")
        save_entry(level, name, message)
    entries = get_entries(level)

    return render_template(
        "modules/xss_stored.html",
        level=level, entries=entries, module="xss_stored",
        current_level=level,
    )
