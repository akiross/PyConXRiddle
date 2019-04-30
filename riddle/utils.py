import sqlite3
import random
from pathlib import Path

from flask import current_app

from riddle import database
from riddle.names import generate_random_animal
from riddle.tools import rot13


help_message = rot13('''\
We managed to inject this message in the unencrypted communication with
the server, but the message might be garbled due to self-defensive
systems.
This is a pledge for help: the WASP10 challenge is staged by an
Evolutionary Artificial Intelligence which took over the WASP10 council.
All us members of the WASP10 are being isolated in any possible way and
none of our messages is going through, but this one.
We hope you found and read this message, because someone hacking
in the system and shutting down the AI is our only hope. The AI is
probably planning to start a global-scale cyber attack aimed to shut
down human digital communications: if it succeeds, it will be chaos.
We are sure that the attack will start on a smaller scale, trying to
interfere with an event which is running *right now* and where many
talented hackers are found, the PyConX Italia. By isolating them, the
AI probably hopes to have and advantage by excluding some of its most
threatening opponents.
But if we stop the AI during this attack to the PyConX, we might be
able to stop it before the global-scale attack starts!
We believe the server where the WASP10 challenge is hosted is the only
public interface of the AI with the world, so we must start from there.
We are sure the system is simple, but robust, and there is not an easy
access, but apparently there are some old entry-points previously used
for computing the statistics of the WASP9 challenge that could be used
to break in. Find them and do your best! We will try to support you
whenever possible, keep your eyes open and send us any relevant message
you find!'''.strip())


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
    current_app.logger.debug(f"Getting files in game folder {current_app.config['GAME_PATH']}")
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
    current_app.logger.debug(f"Checking if level {level} can be accessed.")
    # Get prereq for the level
    req = set(level_prerequisites(str(level)))
    current_app.logger.debug(f"Prerequisites for the level: {req}")
    if not req:
        return True  # No prereq, yay!
    if solved is None:
        solved = set()
    else:
        solved = set(s[1] for s in solved)
    current_app.logger.debug(f"Set of solved levels: {solved}")
    remaining = req - solved
    current_app.logger.debug(f"Remaining to be solved: {remaining}")
    # If nothing remains, user can proceed
    return len(remaining) == 0


def get_graph(id_=None):
    db = database.get_connection()
    if id_ is None:
        rv = db \
            .execute('SELECT * FROM longest_path ORDER BY RANDOM() LIMIT 1') \
            .fetchone()
    else:
        rv = db \
            .execute('SELECT * FROM longest_path where id=?', [id_]) \
            .fetchone()
    if rv is None:
        raise RuntimeError('longest path table not populated')
    return rv


def add_help_message():
    # could also check if sanity is tainted
    if not random.randint(0, 9):  # triggered 10% of the times
        return f'<!--\n{help_message}\n--> p>'
    return ''
