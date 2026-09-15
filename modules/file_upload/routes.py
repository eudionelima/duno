"""modules/file_upload/routes.py"""
from flask import Blueprint, render_template, request, session, redirect, url_for
from core.decorators import login_required
from core.security_levels import get_level


bp = Blueprint("file_upload", __name__)


@bp.route("/file_upload", methods=["GET", "POST"])
@login_required
def index():
    level = get_level(session["user_id"], "file_upload")
    result = None
    if request.method == "POST":
        if "file" not in request.files or request.files["file"].filename == "":
            result = "Nenhum arquivo selecionado."
        else:
            from modules.file_upload.logic import run
            result = run(level, request.files["file"])

    return render_template(
        "modules/file_upload.html",
        level=level, result=result, module="file_upload",
        current_level=level,
    )
