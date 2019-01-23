from pathlib import Path
from unittest import mock
from riddle.utils import get_level_structure, get_level_files


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
        ls = get_level_structure()
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
