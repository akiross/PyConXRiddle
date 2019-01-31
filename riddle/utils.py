import sqlite3
from riddle import database
# from riddle.names import random_animal


def random_animal():
    return "FOOER"


def create_user():
    db = database.get_connection()
    # FIXME this is not great: we could list created users and search for
    # a non-existing one among all possible (shuffled) options
    for _ in range(1000):  # Try 1000 times, just to avoid a deadlock
        try:
            name = random_animal()
            cur = db.execute('INSERT INTO user (name) VALUES (?)',
                             [name])
            db.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            pass  # Retry
    return None


def get_user(user_id):
    db = database.get_connection()
    cur = db.execute('SELECT * FROM user WHERE id = ?',
                     [user_id])
    db.commit()
    # TODO what happens if none is found?
    return cur.fetchone()


def update_user_progress(user_id, level):
    db = database.get_connection()
    db.execute(
        'INSERT INTO progress (user_id, level) values(?,?)',
        [user_id, level])
    db.commit()
