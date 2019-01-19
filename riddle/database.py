import sqlite3

from flask import g, current_app


def create_sqlite_connection():
    conn = sqlite3.connect(
        current_app.config['SQLITE_PATH'],
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    conn.row_factory = sqlite3.Row
    return conn


def get_connection():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = create_sqlite_connection()
    return g._database


def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init():
    db = get_connection()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
