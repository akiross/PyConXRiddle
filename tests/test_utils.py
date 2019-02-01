from pathlib import Path
from unittest import mock
from riddle.utils import (get_level_structure, get_level_files,
    is_user_allowed, strip_common_parents, level_structure_dict,
    level_prerequisites)


def test_level_files():
    with mock.patch('pathlib.Path.glob') as mockglob:
        mockglob.return_value = [
            Path('riddle/game/riddle_1_a.py'),
            Path('riddle/game/riddle_1_b.py'),
            Path('riddle/game/level_2_a/riddle_2_a.py'),
            Path('riddle/game/level_2_a/riddle_2_b.py'),
            Path('riddle/game/level_2_a/level_3_a/riddle_3.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_a.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_b.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_c.py'),
            Path('riddle/game/level_2_b/riddle_2.py'),
        ]
        root, ls = get_level_files()
        assert ls == [
            Path('riddle/game/riddle_1_a.py'),
            Path('riddle/game/riddle_1_b.py'),
            Path('riddle/game/level_2_a/riddle_2_a.py'),
            Path('riddle/game/level_2_a/riddle_2_b.py'),
            Path('riddle/game/level_2_a/level_3_a/riddle_3.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_a.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_b.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_c.py'),
            Path('riddle/game/level_2_b/riddle_2.py'),
        ]


def test_level_structure():
    with mock.patch('riddle.utils.get_level_files') as mockglob:
        mockglob.return_value = Path('riddle/game/'), [
            Path('riddle/game/riddle_1_a.py'),
            Path('riddle/game/riddle_1_b.py'),
            Path('riddle/game/level_2_a/riddle_2_a.py'),
            Path('riddle/game/level_2_a/riddle_2_b.py'),
            Path('riddle/game/level_2_a/level_3_a/riddle_3.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_a.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_b.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_c.py'),
            Path('riddle/game/level_2_b/riddle_2.py'),
        ]
        ls = get_level_structure()
        assert ls == [
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


def test_level_structure_dict():
    with mock.patch('riddle.utils.get_level_files') as mockglob:
        mockglob.return_value = Path('riddle/game/'), [
            Path('riddle/game/riddle_1_a.py'),
            Path('riddle/game/riddle_1_b.py'),
            Path('riddle/game/level_2_a/riddle_2_a.py'),
            Path('riddle/game/level_2_a/riddle_2_b.py'),
            Path('riddle/game/level_2_a/level_3_a/riddle_3.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_a.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_b.py'),
            Path('riddle/game/level_2_a/level_3_b/riddle_3_c.py'),
            Path('riddle/game/level_2_b/riddle_2.py'),
        ]
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
        mockls.return_value = [
            'riddle_1',
            'riddle_2',
            'level_1/riddle',
            'level_2/riddle_1',
            'level_2/riddle_2',
            'level_2/riddle_3',
            'level_2/level_3/riddle_1',
            'level_2/level_3/riddle_2',
        ]

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
            print("TESTING CASE", level, solved, expected)
            assert is_user_allowed(level, solved) == expected

    with mock.patch('riddle.utils.get_level_structure') as mockls:
        mockls.return_value = [
            'riddle_1',
            'riddle_2',
            'level_1/riddle',
            'level_2/riddle_1',
            'level_2/riddle_2',
            'level_2/riddle_3',
            'level_2/level_3/riddle_1',
            'level_2/level_3/riddle_2',
        ]

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
            print("TESTING CASE", level, solved, expected)
            assert is_user_allowed(level, solved) == expected