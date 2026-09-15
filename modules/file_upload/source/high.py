"""modules/file_upload/source/high.py — DUNO source view."""
import os


_ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".gif"}


def handle(file, upload_folder: str) -> str:
    """High: verifica extensão e Content-Type — bypassável com double extension (shell.php.jpg)."""
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in _ALLOWED_EXT:
        return f"Extensão não permitida: {ext}"
    if not file.content_type.startswith("image/"):
        return f"Content-Type inválido: {file.content_type}"
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
