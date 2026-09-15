"""core/source_loader.py — T-013 carregamento de source via importlib+inspect."""
import importlib
import inspect
from flask import jsonify, abort

VALID_LEVELS = ("low", "medium", "high", "impossible")


def load_source(module_name: str, level: str):
    """
    Importa modules.<module>.source.<level> e retorna o código-fonte.
    Segurança: valida module_name contra VALID_MODULES e level contra VALID_LEVELS.
    Não permite path traversal — importlib garante resolução de módulo Python.
    """
    if level not in VALID_LEVELS:
        abort(404)

    # Whitelist de módulos válidos
    from core.security_levels import VALID_MODULES
    if module_name not in VALID_MODULES:
        abort(404)

    try:
        mod = importlib.import_module(f"modules.{module_name}.source.{level}")
        source = inspect.getsource(mod)
        return jsonify({"module": module_name, "level": level, "source": source})
    except ModuleNotFoundError:
        abort(404)
    except Exception:
        abort(500)
