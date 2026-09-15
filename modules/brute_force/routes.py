"""modules/brute_force/routes.py"""
import secrets
from flask import Blueprint, render_template, request, session
from core.decorators import login_required
from core.security_levels import get_level
from modules.brute_force.logic import run

bp = Blueprint("brute_force", __name__)


@bp.route("/brute_force", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "brute_force")
    csrf_token = secrets.token_hex(16)
    session["csrf_token_bf"] = csrf_token
    result = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        submitted_token = request.form.get("csrf_token", "")
        result = run(level, username, password, submitted_token)

    return render_template(
        "modules/brute_force.html",
        level=level,
        result=result,
        csrf_token=csrf_token,
        module="brute_force",
        current_level=level,
    )
