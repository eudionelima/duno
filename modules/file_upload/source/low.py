"""modules/file_upload/source/low.py — DUNO source view."""
import os


def handle(file, upload_folder: str) -> str:
    """Low: salva qualquer arquivo sem verificação — upload de .php direto."""
    filename = file.filename
    path = os.path.join(upload_folder, filename)
    file.save(path)
    return f"Arquivo salvo: {filename}"
