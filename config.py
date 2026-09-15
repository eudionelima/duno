"""T-005 config.py — DUNO configuração central."""
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "duno-insecure-default")
    DATABASE = os.environ.get("DATABASE", "/app/data/duno.db")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB upload limit
    UPLOAD_FOLDER = "/app/static/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "txt"}
    JWT_SECRET = os.environ.get("JWT_SECRET", "duno-jwt-secret")
