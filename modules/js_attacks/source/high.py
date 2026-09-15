"""modules/js_attacks/source/high.py — DUNO source view."""
from core.database import get_db


def handle(product_id: str, submitted_price: str) -> str:
    """High: verifica preço no banco — mas não valida autenticidade do product_id."""
    db = get_db()
    row = db.execute(
        "SELECT value FROM secrets WHERE key=?", (f"price_{product_id}",)
    ).fetchone()
    if not row:
        return "Produto não encontrado."
    expected = float(row["value"])
    submitted = float(submitted_price)
    if abs(submitted - expected) > 0.01:
        return f"Preço inválido. Esperado: R$ {expected:.2f}"
    return f"Compra realizada! Valor: R$ {submitted:.2f}"
