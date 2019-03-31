import sqlite3
from pathlib import Path

from flask import current_app

from riddle import database
from riddle.names import generate_random_animal


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
    user = cur.fetchone()  # Returns user or None
    if user is not None:
        return dict(user)
    return None


def update_user_progress(user_id, level, score=1):
    db = database.get_connection()
    try:
        db.execute(
            'INSERT INTO progress (user_id, level, score) VALUES (?,?,?)',
            [user_id, level, score])
        db.execute(
            'UPDATE user SET score = score + ? WHERE id = ?',
            [score, user_id])
        db.commit()
    except sqlite3.IntegrityError:
        pass  # Progress was already stored


def query_user_progress(user_id):
    db = database.get_connection()
    if user_id is None:
        res = db.execute('SELECT user_id, level, score FROM progress')
    else:
        res = db.execute('SELECT user_id, level, score FROM progress WHERE user_id=?',
                         [user_id])
    yield from ((r[0], r[1], r[2]) for r in res)


def set_user_flag(user_id, flag, value):
    db = database.get_connection()
    try:
        res = db.execute('''INSERT OR REPLACE
                            INTO user_flag (user_id, flag, value)
                            VALUES (?,?,?)''', [user_id, flag, value])
        db.commit()
    except sqlite3.IntegrityError:
        pass


def unset_user_flag(user_id, flag):
    db = database.get_connection()
    try:
        res = db.execute('''DELETE FROM user_flag
                            WHERE user_id=? AND flag=?''',
                            [user_id, flag])
        db.commit()
    except sqlite3.IntegrityError:
        pass


def get_user_flag(user_id, flag):
    db = database.get_connection()
    res = db.execute('''SELECT user_id, flag, value FROM user_flag
                        WHERE user_id=? AND flag=?''', [user_id, flag])
    res = res.fetchone()
    if res is not None:
        return res[2]
    return None


def is_dunder(stem):
    if isinstance(stem, Path):
        stem = stem.stem
    return stem[:2] == '__' and stem[-2:] == '__'


def get_level_files(game_folder):
    """Return the level file paths and their root, as pathlib.Paths."""
    root = Path(game_folder) / 'game'
    return root, root.glob('**/*.py')


def get_level_pathname(fpath, root=None):
    """Given a game file, return its url-path and name in the game."""
    if root is None:
        root, _ = get_level_files(current_app.config['GAME_PATH'])
    else:
        root = Path(root)  # Ensure it's a Path
    fpath = Path(fpath)
    upath = fpath.relative_to(root).parent / fpath.stem
    name = str('.'.join(upath.parts))
    return upath, name


def get_level_structure():
    """Return the url-paths for the levels in the game hierarchy."""
    root, files = get_level_files(current_app.config['GAME_PATH'])
    return [get_level_pathname(fp)[0] for fp in files if not is_dunder(fp)]


def get_level_routes(upath, entry_point):
    """Given the url-path of the level and the entry_point, return its route."""
    def _make_route(r):
        if callable(r):
            return r(upath)
        elif r is None:
            return f'/{upath}'
        return r

    if hasattr(entry_point, 'route'):
        # Call routes that are callable
        routes = [(_make_route(r), d) for r, d in entry_point.route]
    else:
        routes = [(_make_route(None), {})]  # Default route for undecorated EP

    # Fix endpoints
    for rule, options in routes:
        # Use module name as default endpoint
        if 'endpoint' not in options:
            options['endpoint'] = str('.'.join(upath.parts))
    return routes


def level_structure_dict():
    """Return the levels of the game as nested dictionaries."""
    root = {}
    ls = get_level_structure()
    for l in (str(l).split('/') for l in ls):
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
    req = set(level_prerequisites(str(level)))
    if not req:
        return True  # No prereq, yay!
    if solved is None:
        solved = set()
    else:
        solved = set(solved)
    remaining = req - solved
    # If nothing remains, user can proceed
    return len(remaining) == 0
