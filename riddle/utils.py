import os
from riddle import database
from pathlib import Path


def create_user():
    db = database.get_connection()
    cur = db.execute('INSERT INTO user DEFAULT VALUES')
    db.commit()
    return cur.lastrowid


def update_user_progress(user_id, level):
    db = database.get_connection()
    db.execute(
        'INSERT INTO progress (user_id, level) values(?,?)',
        [user_id, level])
    db.commit()


def get_level_files():
    root = Path(__file__).parent / 'game'
    return root, root.glob('**/*.py')


def get_level_structure():
    """Return the levels of the game in hierarchy."""
    root, files = get_level_files()
    return [str((fp.parent / fp.stem).relative_to(root))
            for fp in files]
