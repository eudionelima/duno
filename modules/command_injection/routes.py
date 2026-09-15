"""modules/command_injection/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("command_injection", __name__)


@bp.route("/command_injection", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "command_injection")
    cmd = ""
    result = None
    if request.method == "POST":
        cmd = request.form.get("cmd", "")
        from modules.command_injection.logic import run
        result = run(level, cmd)

    return render_template(
        "modules/command_injection.html",
        level=level, result=result, cmd=cmd, module="command_injection",
        current_level=level,
    )
