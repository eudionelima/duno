"""modules/file_upload/source/medium.py — DUNO source view."""
import os


_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/gif"}


def handle(file, upload_folder: str) -> str:
    """Medium: verifica Content-Type — bypassável via Burp alterando o header."""
    if file.content_type not in _ALLOWED_TYPES:
        return f"Tipo não permitido: {file.content_type}"
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
