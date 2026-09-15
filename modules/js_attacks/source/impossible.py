"""modules/js_attacks/source/impossible.py — DUNO source view."""


_CATALOG = {
    "1": 99.90,
    "2": 199.90,
    "3": 49.90,
}


def handle(product_id: str) -> str:
    """Impossible: preço definido exclusivamente no servidor — cliente não envia valor."""
    price = _CATALOG.get(product_id)
    if price is None:
        return "Produto não encontrado."
    return f"Compra realizada! Valor: R$ {price:.2f}"
