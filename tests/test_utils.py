import pytest
import sqlite3

from pathlib import Path
from unittest import mock
from riddle import database
from riddle.utils import get_user_flag
from riddle.utils import set_user_flag
from riddle.utils import get_level_files
from riddle.utils import is_user_allowed
from riddle.utils import unset_user_flag
from riddle.utils import get_level_routes
from riddle.utils import get_level_structure
from riddle.utils import level_prerequisites
from riddle.utils import query_user_progress
from riddle.utils import level_structure_dict
from riddle.utils import strip_common_parents
from riddle.utils import update_user_progress


example_levels = [
    'riddle_1_a',
    'riddle_1_b',
    'level_2_a/riddle_2_a',
    'level_2_a/riddle_2_b',
    'level_2_a/level_3_a/riddle_3',
    'level_2_a/level_3_b/riddle_3_a',
    'level_2_a/level_3_b/riddle_3_b',
    'level_2_a/level_3_b/riddle_3_c',
    'level_2_b/riddle_2',
]


example_levels_2 = [
    'riddle_1',
    'riddle_2',
    'level_1/riddle',
    'level_2/riddle_1',
    'level_2/riddle_2',
    'level_2/riddle_3',
    'level_2/level_3/riddle_1',
    'level_2/level_3/riddle_2',
]


def test_level_files():
    file_list = [Path('riddle/game') / f'{l}.py' for l in example_levels]

    with mock.patch('pathlib.Path.glob') as mockglob:
        mockglob.return_value = file_list
        root, ls = get_level_files()
        assert ls == file_list


def test_level_structure():
    file_list = [Path('riddle/game') / f'{l}.py' for l in example_levels]

    with mock.patch('riddle.utils.get_level_files') as mockglob:
        mockglob.return_value = Path('riddle/game/'), file_list
        ls = get_level_structure()
        assert [str(l) for l in ls] == example_levels


def test_level_structure_dict():
    file_list = [Path('riddle/game') / f'{l}.py' for l in example_levels]

    with mock.patch('riddle.utils.get_level_files') as mockglob:
        mockglob.return_value = Path('riddle/game/'), file_list
        ls = level_structure_dict()
        assert ls == {
            'riddle_1_a': None,
            'riddle_1_b': None,
            'level_2_a': {
                'riddle_2_a': None,
                'riddle_2_b': None,
                'level_3_a': {
                    'riddle_3': None,
                },
                'level_3_b': {
                    'riddle_3_a': None,
                    'riddle_3_b': None,
                    'riddle_3_c': None,
                },
            },
            'level_2_b': {
                'riddle_2': None,
            },
        }


def test_strip_common_parents():
    cases = [
        [['a', 'b', 'c'], ['a', 'b', 'c'], ''],
        [['a', 'a/b', 'a/c'], ['a', 'a/b', 'a/c'], ''],  # Same name file/dir
        [['p/a', 'p/b', 'p/c/d'], ['a', 'b', 'c/d'], 'p'],
        [['a', 'b/b', 'c/c'], ['a', 'b/b', 'c/c'], ''],
        [['p/p/a/a', 'p/p/a/b', 'p/p/c'], ['a/a', 'a/b', 'c'], 'p/p'],
    ]

    for levels, expected, expected_common in cases:
        common, new_levels = strip_common_parents(levels)
        assert set(new_levels) == set(expected)
        assert common == expected_common


def test_level_prerequisites():
    with mock.patch('riddle.utils.get_level_structure') as mockls:
        mockls.return_value = example_levels_2

        cases = [
            ['riddle_1', []],
            ['riddle_2', []],
            ['level_1/riddle', ['riddle_1', 'riddle_2']],
            ['level_2/riddle_1', ['riddle_1', 'riddle_2']],
            ['level_2/riddle_2', ['riddle_1', 'riddle_2']],
            ['level_2/riddle_3', ['riddle_1', 'riddle_2']],
            ['level_2/level_3/riddle_1', [
                'riddle_1',
                'riddle_2',
                'level_2/riddle_1',
                'level_2/riddle_2',
                'level_2/riddle_3',
            ]],
        ]

        for level, prereq in cases:
            print("TESTING CASE", level, prereq)
            assert set(level_prerequisites(level)) == set(prereq)


def test_user_access():
    with mock.patch('riddle.utils.get_level_structure') as mockls:
        mockls.return_value = [
            'riddle',
            'level/riddle',
        ]

        cases = [
            ['riddle', [], True],
            ['riddle', ['riddle'], True],
            ['riddle', ['riddle', 'level/riddle'], True],
            ['level/riddle', [], False],
            ['level/riddle', ['riddle'], True],
            ['level/riddle', ['riddle', 'level/riddle'], True],
        ]
        for level, solved, expected in cases:
            assert is_user_allowed(level, solved) == expected

    with mock.patch('riddle.utils.get_level_structure') as mockls:
        mockls.return_value = example_levels_2

        cases = [
            ['riddle_1', [], True],
            ['riddle_2', [], True],
            ['riddle_1', ['riddle_1'], True],
            ['riddle_2', ['riddle_1'], True],
            ['riddle_2', [
                'riddle_1',
                'level_1/riddle',
                'level_2/riddle_2',
            ], True],
            ['riddle_2', [
                'riddle_1',
                'level_1/riddle',
                'level_2/riddle_2',
                'level_2/level_3/riddle_1',
            ], True],
            ['level_1/riddle', [], False],
            ['level_1/riddle', ['riddle_1'], False],
            ['level_1/riddle', ['riddle_2'], False],
            ['level_1/riddle', ['level_1/riddle'], False],
            ['level_1/riddle', ['riddle_1', 'riddle_2'], True],
            ['level_2/riddle_1', ['riddle_1', 'riddle_2'], True],
            ['level_2/riddle_2', ['riddle_1', 'riddle_2'], True],
            ['level_2/riddle_3', ['riddle_1', 'riddle_2'], True],
            ['level_2/level_3/riddle_1', ['riddle_1', 'riddle_2'], False],
            ['level_2/level_3/riddle_2', [
                'riddle_1',
                'riddle_2',
                'level_1/riddle',
                'level_2/riddle_1',
                'level_2/riddle_2',
                ], False],
        ]

        for level, solved, expected in cases:
            assert is_user_allowed(level, solved) == expected

    # Ensure dunder files are ignored in the level structure
    with mock.patch('riddle.utils.get_level_files') as mockfp:
        mockfp.return_value = Path('/riddle/game'), [
            Path('/riddle/game/__foo__.py'),
            Path('/riddle/game/foo/foo.py'),
            Path('/riddle/game/bar/bar.py'),
        ]

        cases = [
            ['foo/foo', [], True],
            ['bar/bar', [], True],
            ['foo/foo', ['bar/bar'], True],
            ['bar/bar', ['foo/foo'], True],
        ]
        for level, solved, expected in cases:
            assert is_user_allowed(level, solved) == expected


def test_level_routing():
    def _ep():
        return 'this is the entry point'

    # Ensure that when the (undecorated) entry-point has no route attr, the
    # returned route is the path plus a standard endpoint
    for l, p in zip(example_levels, map(Path, example_levels)):
        endpoint = {'endpoint': '.'.join(p.parts)}
        assert get_level_routes(p, _ep) == [(f'/{l}', endpoint)]

    # Check that when endpoint is decorated with a value, that value is used
    # as the URL. If endpoint is missing, a default is used
    for l, p in zip(example_levels, map(Path, example_levels)):
        # Set this at every loop so we get a clean state every time
        _ep.route = [('/this/is/a/upath', {})]
        endpoint = {'endpoint': '.'.join(p.parts)}
        assert get_level_routes(p, _ep) == [('/this/is/a/upath', endpoint)]

    # Check that, if the entry point is given, it is used correctly
    for l, p in zip(example_levels, map(Path, example_levels)):
        # Set this at every loop so we get a clean state every time
        _ep.route = [('/this/is/a/upath', {'endpoint': l[:2] + l[-2:]})]
        endpoint = {'endpoint': l[:2] + l[-2:]}
        assert get_level_routes(p, _ep) == [('/this/is/a/upath', endpoint)]

    # Check that if route is callable, it is invoked and used
    for l, p in zip(example_levels, map(Path, example_levels)):
        # Set this at every loop so we get a clean state every time
        _ep.route = [(lambda up: up / 'foo', {})]
        endpoint = {'endpoint': '.'.join(p.parts)}
        assert get_level_routes(p, _ep) == [(p / 'foo', endpoint)]

    # Check that multiple routes of different nature might be present
    for l, p in zip(example_levels, map(Path, example_levels)):
        # Set this at every loop so we get a clean state every time
        _ep.route = [(lambda up: up / 'foo', {}),
                     ('/a/upath', {})]
        endpoint = {'endpoint': '.'.join(p.parts)}
        assert get_level_routes(p, _ep) == [(p / 'foo', endpoint),
                                            ('/a/upath', endpoint)]


def test_user_progress():
    # Create sqlite in memory
    with mock.patch('riddle.database.get_connection') as mockconn:
        conn = sqlite3.connect(':memory:')
        conn.executescript(open('riddle/schema.sql', 'rt').read())
        mockconn.return_value = conn

        users = ['user0', 'user1']
        levels = [f'/mock/levels/{i}' for i in range(4)]
        # Initially there is no progress 
        assert sorted(query_user_progress(users[0])) == []

        # The progress can be added to the database
        update_user_progress(users[0], levels[0])
        assert sorted(query_user_progress(users[0])) == [(users[0], levels[0])]
         
        # Duplicated entries should not occurr
        update_user_progress(users[0], levels[0])
        assert sorted(query_user_progress(users[0])) == [(users[0], levels[0])]

        # Multiple entries are ok
        update_user_progress(users[0], levels[1])
        assert sorted(query_user_progress(users[0])) == [(users[0], levels[0]),
                                                         (users[0], levels[1])]

        # Having multiple users should be no problem
        update_user_progress(users[1], levels[0])
        update_user_progress(users[1], levels[2])
        update_user_progress(users[0], levels[3])
        assert sorted(query_user_progress(users[0])) == [(users[0], levels[0]),
                                                         (users[0], levels[1]),
                                                         (users[0], levels[3])]

        assert sorted(query_user_progress(users[1])) == [(users[1], levels[0]),
                                                         (users[1], levels[2])]

        # We should be able to query all users
        assert sorted(query_user_progress(None)) == [(users[0], levels[0]),
                                                     (users[0], levels[1]),
                                                     (users[0], levels[3]),
                                                     (users[1], levels[0]),
                                                     (users[1], levels[2])]


def test_user_flag():
    # Create sqlite in memory
    with mock.patch('riddle.database.get_connection') as mockconn:
        conn = sqlite3.connect(':memory:')
        conn.executescript(open('riddle/schema.sql', 'rt').read())
        mockconn.return_value = conn

        users = ['user0', 'user1']
        # levels = [f'/mock/levels/{i}' for i in range(4)]
        flags = [f'flag{i}' for i in range(4)]
        values = [f'value{i}' for i in range(4)]

        # Values default to None
        assert get_user_flag(users[0], flags[0]) is None

        # Values can be set
        set_user_flag(users[0], flags[0], values[0])
        assert get_user_flag(users[0], flags[0]) == values[0]

        # Values are updated correctly
        set_user_flag(users[0], flags[0], values[1])
        assert get_user_flag(users[0], flags[0]) == values[1]

        # Values can be unset
        unset_user_flag(users[0], flags[0])
        assert get_user_flag(users[0], flags[0]) is None
