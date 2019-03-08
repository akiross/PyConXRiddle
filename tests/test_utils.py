from pathlib import Path
from unittest import mock
from riddle.utils import (get_level_structure, get_level_files,
    is_user_allowed, strip_common_parents, level_structure_dict,
    level_prerequisites, get_level_route)


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

example_entry_points = [
    'foo'
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
    for l in example_levels:
        print("Level", l)
        assert get_level_route(l, lambda: 'foo') == [('/' + l, {})]
