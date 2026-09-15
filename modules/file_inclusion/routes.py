"""modules/file_inclusion/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level

from modules.file_inclusion.logic import setup_pages as _setup_pages

bp = Blueprint("file_inclusion", __name__)


@bp.route("/file_inclusion", methods=["GET"])
@login_required
def index():
    level = get_level(session["user_id"], "file_inclusion")
    page = request.args.get("page", "")
    result = None
    _setup_pages()
    if page:
        from modules.file_inclusion.logic import run
        result = run(level, page)

    return render_template(
        "modules/file_inclusion.html",
        level=level, result=result, page=page, module="file_inclusion",
        current_level=level,
    )
