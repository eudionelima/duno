"""modules/js_attacks/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("js_attacks", __name__)


@bp.route("/js_attacks", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "js_attacks")
    result = None
    if request.method == "POST":
        product_id = request.form.get("product_id", "1")
        price = request.form.get("price", "")
        from modules.js_attacks.logic import run
        result = run(level, product_id, price)

    return render_template(
        "modules/js_attacks.html",
        level=level, result=result, module="js_attacks",
        current_level=level,
    )
