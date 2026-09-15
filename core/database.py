"""core/database.py — T-010 conexão SQLite."""
import sqlite3
import os
from flask import g, current_app


def get_db():
    """Retorna conexão SQLite para o contexto da requisição."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Registra close_db no teardown da aplicação."""
    app.teardown_appcontext(close_db)
