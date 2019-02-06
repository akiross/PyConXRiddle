import os
import sqlite3
from riddle import database
from pathlib import Path
from riddle.names import random_animal, generate_random_animal


def create_user():
    db = database.get_connection()
    # Generate random names
    for name in generate_random_animal(sep='-'):
        try:
            cur = db.execute('INSERT INTO user (name) VALUES (?)',
                             [name])
            db.commit()
            return cur.lastrowid
        except sqlite3.IntegrityError:
            pass  # Retry with next name
    return None


def get_user(user_id):
    db = database.get_connection()
    cur = db.execute('SELECT * FROM user WHERE id = ?',
                     [user_id])
    db.commit()
    return cur.fetchone()  # Returns user or None


def update_user_progress(user_id, level):
    db = database.get_connection()
    try:
        db.execute(
            'INSERT INTO progress (user_id, level) values(?,?)',
            [user_id, level])
        db.commit()
    except sqlite3.IntegrityError:
        pass  # Progress was already stored


def query_user_progress(user_id):
    db = database.get_connection()
    if user_id is None:
        res = db.execute('SELECT user_id, level FROM progress')
    else:
        res = db.execute('SELECT user_id, level FROM progress WHERE user_id=?',
                         [user_id])
    yield from ((r['user_id'], r['level']) for r in res)


def get_level_files():
    root = Path(__file__).parent / 'game'
    return root, root.glob('**/*.py')


def get_level_structure():
    """Return the levels of the game in hierarchy."""
    root, files = get_level_files()
    return [str((fp.parent / fp.stem).relative_to(root))
            for fp in files]


def level_structure_dict():
    """Return the levels of the game as nested dictionaries."""
    root = {}
    ls = get_level_structure()
    for l in (l.split('/') for l in ls):
        cur_tree = root
        for d in l[:-1]:
            cur_tree = cur_tree.setdefault(d, {})
        cur_tree[l[-1]] = None
    return root


def strip_common_parents(levels):
    """Return a cope of levels where the common parents are stripped."""
    print("Stripping common parents from:", levels)
    # Split by folder
    levels = [l.split('/') for l in levels]
    common_parents = []
    while True:
        # Compute what is left in the levels if we remove the 1st part
        roots, residuals = zip(*((l[0], l[1:]) for l in levels))
        # If roots are the same and residuals are all non-empy
        if len(set(roots)) == 1 and all(residuals):
            common_parents.append(roots[0])
            levels = residuals  # Continue iteratively stripping next level
        else:
            # No more common parents
            return '/'.join(common_parents), set('/'.join(l) for l in levels)


def level_prerequisites(level):
    """Compute the levels that must be completed before accessing level."""
    def is_level_in(level, ls):
        d = ls
        for l in level.split('/'):
            if l in d:
                d = d[l]
            else:
                return False
        return d is None

    # Get current game structure as dicts
    ls = level_structure_dict()
    # Check if level is valid
    if not is_level_in(level, ls):
        raise ValueError("Level does not belong to this game")

    level = level.split('/')
    if len(level) == [0]:
        raise RuntimeError("WAT level cannot be empty!")
    if len(level) == 1:
        return []  # No prerequisites for levels in the root

    # Locate all dependencies
    d = ls
    deps = []
    tree = []
    for l in level[:-1]:  # Skip level itself
        # Find all dependencies for l
        for k, v in d.items():
            if v is None:
                deps.append('/'.join(tree + [k]))
        tree.append(l)  # Save path
        d = d[l]  # Lower level

    return deps


def is_user_allowed(level, solved):
    """Given a list of solved riddles, return True if user can access level."""
    # Get prereq for the level
    req = set(level_prerequisites(level))
    if not req:
        return True  # No prereq, yay!
    if solved is None:
        solved = set()
    else:
        solved = set(solved)
    remaining = req - solved
    # If nothing remains, user can proceed
    return len(remaining) == 0
