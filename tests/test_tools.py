import pytest

from riddle import tools


@pytest.mark.parametrize('shift,input_string,expected', [
    (1, 'abcdefghijklmnopqrstuvwxyz', 'bcdefghijklmnopqrstuvwxyza'),
    (2, 'abcdefghijklmnopqrstuvwxyz', 'cdefghijklmnopqrstuvwxyzab'),
    (13, 'abcdefghijklmnopqrstuvwxyz', 'nopqrstuvwxyzabcdefghijklm'),
    (13, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'NOPQRSTUVWXYZABCDEFGHIJKLM'),
    (26, 'abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz'),
    (27, 'abcdefghijklmnopqrstuvwxyz', 'bcdefghijklmnopqrstuvwxyza'),
    (
        3,
        'the quick brown fox jumps over the lazy dog!',
        'wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj!'
    ),
    (
        3,
        'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!',
        'WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ!'
    ),
    (
        21,
        'the quick brown fox jumps over the lazy dog!',
        'ocz lpdxf wmjri ajs ephkn jqzm ocz gvut yjb!'
    ),
])
def test_caesar(shift, input_string, expected):
    assert tools.caesar(input_string, shift) == expected
    if shift == 13:
        assert tools.rot13(input_string) == expected


@pytest.mark.parametrize('alphabet,shift,input_string,expected', [
    ('abc', 0, 'abc', 'abc'),
    ('abc', 1, 'abc', 'bca'),
    ('abc', 2, 'abc', 'cab'),
    ('abc', 3, 'abc', 'abc'),
])
def test_caesar_sym(alphabet, shift, input_string, expected):
    # Test string alphabet
    assert tools.caesar(input_string, shift, alphabet) == expected
    # Test callable alphabet
    assert tools.caesar(input_string, shift, lambda: (alphabet,)) == expected


@pytest.mark.parametrize('bits_list,rule,boundary,expected', [
    # TODO test exception is raised with invalid values
    # test invalid boundary
    # test invalid values in list/string (wrong type, wrong balues, etc)
    # Ensure types are correct for input and output
    ('0101', 51, '0', '0101'),  # str to str
    ([0, 1, 0, 1], 51, '0', [0, 1, 0, 1]),  # list(int) to list(int)
    # Test few rules
    ('0101', 51, '0', '0101'),
    ('1111', 51, '1', '1111'),
    ('1001', 51, 'extend', '1001'),
    ('0111', 51, 'loop', '0111'),
    ('0101', 0, 'loop', '0000'),
    ('0101', 0, 'even', '0000'),
    ('0101', 0, 'odd', '0000'),
    # Test boundaries
    ('0101', 30, 'loop', '1010'),  # input is like 1|0101|0
    ('0101', 30, 'extend', '0011'),  # input is like 0|0101|1
    ('0101', 30, 'even', '1010'),  # input is like 1|0101|0
    ('0101', 30, 'odd', '0011'),  # input is like 0|0101|1
    ('0101', 30, 'zero', '0010'),  # input is like 0|0101|0
    ('0101', 30, 'one', '1011'),  # input is like 1|0101|1
])
def test_cell_automata(bits_list, rule, boundary, expected):
    # Some rules to test:
    # rule 0 -> always return Y=0
    # rule 255 -> always return Y=1
    # rule 51 -> identity Y=X (A)
    # rule 30 -> chaotic
    # xXx | A | B | ? |   | ...
    # ----+---+---+---+---+---
    # 000 | 0 | 0 | 0 | 0 | 0
    # 001 | 0 | 0 | 0 | 0 | 0
    # 010 | 1 | 0 | 0 | 0 | 1
    # 011 | 1 | 1 | 0 | 0 | 1
    # 100 | 0 | 1 | 0 | 0 | 0
    # 101 | 0 | 1 | 0 | 0 | 0
    # 110 | 1 | 1 | 0 | 0 | 1
    # 111 | 1 | 0 | 0 | 0 | 1
    assert tools.ca1D_step(bits_list, rule, boundary) == expected


def test_cantor_generate():
    positions = [
        (0, 0),
        (0, 1), (1, 0),
        (2, 0), (1, 1), (0, 2),
        (0, 3), (1, 2), (2, 1), (3, 0),
    ]

    for c, p in zip(tools.cantor_generate(), positions):
        assert c == p


def test_cantor_enum():
    pairs = [
        (0, (0, 0)),
        (1, (0, 1)),
        (2, (1, 0)),
        (3, (2, 0)),
        (4, (1, 1)),
        (5, (0, 2)),
        (6, (0, 3)),
        (7, (1, 2)),
        (8, (2, 1)),
        (9, (3, 0)),
    ]

    for i, pos in pairs:
        assert tools.cantor_position(i) == pos

    for i, pos in zip(range(100), tools.cantor_generate()):
        assert tools.cantor_position(i) == pos


def test_dumb_primality_test():
    primes_under_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                        53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    putative_primes = [i for i in range(2, 101) if tools.dumb_primality_test(i)]
    assert primes_under_100 == putative_primes


def test_sieve_of_eratosthenes():
    n = 10
    prime_list = [i for i in range(2, n+1) if tools.dumb_primality_test(i)]
    assert tools.sieve_of_eratosthenes(n) == prime_list


def test_prime_generator():
    n = 100
    primes = tools.sieve_of_eratosthenes(n)
    for i, p in zip(tools.prime_generator(), primes):
        assert i == p


@pytest.mark.parametrize('value,expansion', [
    ((0, 3), (0, 0, 0)),
    ((1, 3), (0, 0, 1)),
    ((2, 3), (0, 1, 0)),
    ((3, 3), (0, 1, 1)),
    ((4, 3), (1, 0, 0)),
    ((5, 3), (1, 0, 1)),
    ((6, 3), (1, 1, 0)),
    ((7, 3), (1, 1, 1)),
    ((7, 4), (0, 1, 1, 1)),
    ((9, 4), (1, 0, 0, 1)),
])
def test_bits_to_tuple(value, expansion):
    assert tools.bits_to_tuple(*value) == expansion
