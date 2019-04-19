"""This is a poorly coded statistics page that gives user info."""

import zlib
import random
import sqlite3
import datetime

from pathlib import Path
from jinja2 import Template
from flask import session, request, current_app

from riddle.names import random_name, _names, _adjectives
from riddle.utils import create_user, get_user
from riddle.urls import without_answer, add_route


super_user = ("monty-python", "flying circus")


success_message = f'''
If you are reading this message, it means you made it: I am {super_user[0]},
one of the funding members of the WASP10 association and I found the hole in
the system that you just exploited to get this message. Sorry if we were not
very explicit in telling how to come here, but trust is fundamental in this
phase. I would like to let you know that you are not alone, and the number of
people fighting the EAI must continue growing.
At the venue, there are some WASP10 undercover agents that have been sent there
to scout talents and invite them to participate in the competition. Those
agents are still unaware of the fact that an EAI overtook our communications.
Your job is now to find them and inform them of what is happening.
You must gain their trust and let them know the truth. They will give you the
necessary information to break into the system and break the AI. When you find
them, don't forget my name.
Good luck.
'''
# But... WASP10 is now public, why having undercover agents? Why do they need
# to trust the player?? This is fishy...

# Let's use the same join date to keep it simple and fishy
join_date = "2009-10-30"

hosts = (
    # Actually interesting hosts
    (1, '127.0.0.1', 'telnet'),  # User connects here to get a message
    (2, '5.44.12.71', 'http'),  # id=2 will be used by retrieve.php
    # Some random hosts
    # (3, '5.44.12.70', 'ftp'),
    # (4, '1.32.1.32', 'irc'),  # This could actually be real :)
    # (5, '10.42.0.112', 'pop3'),
    # Some not-so-random hosts, just for fun
    (6, '20.19.5.2', 'pcx'),
    (7, '20.19.5.3', 'pcx'),
    (8, '20.19.5.4', 'pcx'),
    (9, '20.19.5.5', 'pcx'),
)

# Let's give PyConX organizers some credit :)
users = (
    ('patrick91', "thank you for the birthday gift, marilyn"),
    ('davidmugnai', "measure once, cut once, fix once"),
    ('hype_fi', "impossible is just a matter of time"),
    ('simbasso', "we should not test in production"),
    ('cm', "the glass is half full and half wrong"),
    ('yakkys', "d-j-a-n-g-o, the d is silent"),
    ('mena', "go go gadget everything"),
    ('leriomaggio', "from oxford import british_accent"),
    ('__pamaron__', ""),
    ('viperale', ""),
    # TODO add others!
    super_user,  # Easily breakable
)


def get_database(user):
    """Return the database of a given user, making it up if not existing."""
    root = Path('./data')
    root.mkdir(parents=True, exist_ok=True)

    db_file = root / f'db_{user["id"]}.sqlite3'
    if db_file.exists():
        print("Loading existing db")
        db = sqlite3.connect(db_file)
        return db

    print("Creating database for user", user)
    db = sqlite3.connect(db_file)
    with db:
        # Seed random number generation uniquely for each player for coherent xp
        rng = random.Random()
        rng.seed(user['id'])

        # Generate some random players with unique name
        num_fake_players = rng.randrange(50, 70)
        fake_player_names = {random_name('-', rng)
                             for _ in range(num_fake_players)}
        # Add one user which is particular... Why would WASP9 use a special
        # python-related name? This is fishy...
        fake_player_names.add(super_user[0])

        # Build a (deterministically) shuffled list of uers
        # user_data = {name: ['2009-10-30'] for name in fake_player_names}
        usernames = sorted(fake_player_names)
        rng.shuffle(usernames)

        db.executescript('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE event (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                origin INTEGER NOT NULL,
                value INTEGER NOT NULL,
                timestamp TIMESTAMP NOT NULL
            );

            CREATE TABLE counter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT NOT NULL,
                count INTEGER NOT NULL
            );

            CREATE TABLE hosts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                host TEXT NOT NULL,
                protocol TEXT NOT NULL
            );

            CREATE TABLE actl (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL UNIQUE,
                crc TEXT NOT NULL
            );
        ''')

        for usr in usernames:
            db.execute('''INSERT INTO user (name, timestamp) VALUES (?,?)''',
                        [usr, join_date])

        for ev in ['access', 'access', 'score', 'score']:
            db.execute('''INSERT INTO event (name, origin, value, timestamp)
                           VALUES (?,?,?,?)''',
                           ['access', 'wasp9/stage0', 1, '2009-02-02'])

        for n in [(1, 1), (2, 75), (3, 112)]:
            db.execute('''INSERT INTO counter (event_id, count)
                          VALUES (?,?)''',
                          n)

        for h in hosts:
            db.execute('''INSERT INTO hosts (id, host, protocol)
                          VALUES (?,?,?)''', h)

        for user, pwd in users:
            db.execute('''INSERT INTO actl (user, crc) VALUES (?,?)''', 
                       [user, zlib.crc32(pwd.encode())])

    return db