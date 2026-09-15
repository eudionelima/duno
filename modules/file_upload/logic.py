"""modules/file_upload/logic.py"""
from flask import current_app
from modules.file_upload.source import low, medium, high, impossible


def run(level: str, file) -> str:
    folder = current_app.config["UPLOAD_FOLDER"]
    if level == "low":    return low.handle(file, folder)
    if level == "medium": return medium.handle(file, folder)
    if level == "high":   return high.handle(file, folder)
    return impossible.handle(file, folder)
