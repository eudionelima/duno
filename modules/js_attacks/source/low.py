"""modules/js_attacks/source/low.py — DUNO source view."""


def handle(price: str) -> str:
    """Low: valor de preço validado somente no JS cliente — manipulável via DevTools."""
    try:
        p = float(price)
        return f"Compra realizada! Valor pago: R$ {p:.2f}"
    except ValueError:
        return "Valor inválido."
