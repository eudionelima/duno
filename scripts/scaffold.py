#!/usr/bin/env python3
"""Script para criar estrutura boilerplate de todos os módulos DUNO."""
import os

MODULES = [
    "brute_force", "command_injection", "csrf", "file_inclusion",
    "file_upload", "captcha", "sqli", "sqli_blind", "weak_session",
    "xss_dom", "xss_reflected", "xss_stored", "csp_bypass", "js_attacks",
    "auth_bypass", "open_redirect", "crypto", "api_versioning",
    "mass_assignment", "api_security",
]

BASE = "/home/dione/Projects/duno/modules"

for mod in MODULES:
    mod_dir = os.path.join(BASE, mod)
    src_dir = os.path.join(mod_dir, "source")
    os.makedirs(src_dir, exist_ok=True)

    # __init__.py
    init = os.path.join(mod_dir, "__init__.py")
    if not os.path.exists(init):
        with open(init, "w") as f:
            f.write(f'"""modules/{mod}/__init__.py"""\n')
            f.write(f'from modules.{mod}.routes import bp\n')
            f.write(f'__all__ = ["bp"]\n')

    # source files
    for level in ["low", "medium", "high", "impossible"]:
        src_file = os.path.join(src_dir, f"{level}.py")
        if not os.path.exists(src_file):
            with open(src_file, "w") as f:
                f.write(f'"""modules/{mod}/source/{level}.py — DUNO source view."""\n\n\n')
                f.write(f'def handle(request):\n')
                f.write(f'    """Implementação {level} do módulo {mod}."""\n')
                f.write(f'    pass\n')

    print(f"[ok] {mod}")

print("Estrutura criada.")
