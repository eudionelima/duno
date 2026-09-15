"""modules/js_attacks/source/medium.py — DUNO source view."""


_MIN_PRICE = 99.90


def handle(price: str) -> str:
    """Medium: valida server-side mas compara float — manipulável com precisão."""
    try:
        p = float(price)
        if p < 0:
            return "Valor negativo não permitido."
        return f"Compra realizada! Valor pago: R$ {p:.2f}"
    except ValueError:
        return "Valor inválido."
