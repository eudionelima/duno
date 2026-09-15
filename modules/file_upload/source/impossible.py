"""modules/file_upload/source/impossible.py — DUNO source view."""
import os
import uuid
from PIL import Image
import io


def handle(file, upload_folder: str) -> str:
    """Impossible: valida magic bytes via PIL + renomeia com UUID + recomprime imagem."""
    try:
        data = file.read()
        img = Image.open(io.BytesIO(data))
        img.verify()  # raises se não for imagem válida
    except Exception:
        return "Arquivo não é uma imagem válida."

    file.seek(0)
    try:
        img = Image.open(io.BytesIO(file.read()))
        img = img.convert("RGB")
    except Exception:
        return "Erro ao processar imagem."

    safe_name = uuid.uuid4().hex + ".jpg"
    path = os.path.join(upload_folder, safe_name)
    img.save(path, "JPEG", quality=85)
    return f"Imagem salva com segurança: {safe_name}"
