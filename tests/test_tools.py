from riddle import tools


def test_caesar():
    cases = [
        (1, 'abcdefghijklmnopqrstuvwxyz', 'bcdefghijklmnopqrstuvwxyza'),
        (2, 'abcdefghijklmnopqrstuvwxyz', 'cdefghijklmnopqrstuvwxyzab'),
        (13, 'abcdefghijklmnopqrstuvwxyz', 'nopqrstuvwxyzabcdefghijklm'),
        (13, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'NOPQRSTUVWXYZABCDEFGHIJKLM'),
        (26, 'abcdefghijklmnopqrstuvwxyz', 'abcdefghijklmnopqrstuvwxyz'),
        (27, 'abcdefghijklmnopqrstuvwxyz', 'bcdefghijklmnopqrstuvwxyza'),
        (3, 'the quick brown fox jumps over the lazy dog!',
            'wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj!'),
        (3, 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!',
            'WKH TXLFN EURZQ IRA MXPSV RYHU WKH ODCB GRJ!'),
        (21, 'the quick brown fox jumps over the lazy dog!',
             'ocz lpdxf wmjri ajs ephkn jqzm ocz gvut yjb!'),
    ]

    for n, a, r in cases:
        assert tools.caesar(a, n) == r
        if n == 13:
            assert tools.rot13(a) == r


def test_cell_automata():
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

    cases = [
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
    ]
    for l, r, b, e in cases:
        assert tools.ca1D_step(l, r, b) == e


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
