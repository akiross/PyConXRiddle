from unittest import mock
from riddle.utils import get_level_structure


def test_level_structure():
    with mock.patch('os.walk') as mockwalk:
        mockwalk.return_value = [
            ('riddle/game', ['level_2_a', 'level_2_b'], ['riddle_1_b.py', 'riddle_1_a.py']),
            ('riddle/game/level_2_a', ['level_3_b', 'level_3_a'], ['riddle_2_b.py', 'riddle_2_a.py']),
            ('riddle/game/level_2_a/level_3_b', [], ['riddle_3_b.py', 'riddle_3_c.py', 'riddle_3_a.py']),
            ('riddle/game/level_2_a/level_3_a', [], ['riddle_3.py']),
            ('riddle/game/level_2_b', [], ['riddle_2.py'])
        ]
        print(get_level_structure())
    print(get_level_structure())
    #assert ls is not None
    assert False
