"""modules/captcha/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("captcha", __name__)


@bp.route("/captcha", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "captcha")
    from modules.captcha.logic import get_challenge, run
    challenge = get_challenge(level)
    result = None
    if request.method == "POST":
        challenge_id = request.form.get("challenge_id", "")
        answer = request.form.get("answer", "")
        result = run(level, challenge_id, answer)

    return render_template(
        "modules/captcha.html",
        level=level, result=result, challenge=challenge, module="captcha",
        current_level=level,
    )
