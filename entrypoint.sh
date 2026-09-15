#!/bin/sh
# T-004 entrypoint.sh — DUNO
set -e

echo "============================================"
echo " DUNO — Designed Unsecure Network Operations"
echo " http://localhost:2300"
echo "============================================"

mkdir -p /app/data /app/static/uploads

# seed only if db does not exist
if [ ! -f /app/data/duno.db ]; then
    echo "[entrypoint] Banco não encontrado — executando seed.py..."
    python seed.py
    echo "[entrypoint] Seed concluído."
else
    echo "[entrypoint] Banco encontrado — pulando seed."
fi

echo "[entrypoint] Iniciando Flask na porta 2300..."
exec python run.py
