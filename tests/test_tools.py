import pytest

from PIL import Image
from riddle import tools
from itertools import product


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


@pytest.mark.parametrize('write_seq, read_seq', [
    (b'\x00\x00\x00', b'\x00\x00\x00'),
    (b'\x01\x02\x03', b'\x01\x02\x03'),
    (b'\x10\x20\x30', b'\x10\x20\x30'),
])
def test_seq_steganography(write_seq, read_seq):
    # Build a matrix as image
    seq = (0x0, 0x1, 0x2, 0x4, 0x8)
    image_data = bytes(a * 0x10 + b for a, b in product(seq, repeat=2))
    img = Image.frombytes('L', (len(seq), len(seq)), image_data)
    # Write bytes to image (ensure data will fit)
    assert len(write_seq) * 8 <= len(seq) * len(seq)
    steg_img = tools.write_to_image_bit(img, write_seq)
    # Read bytes from image, but crop trailing bytes
    assert read_seq == tools.read_from_image_bit(steg_img)[:len(read_seq)]


@pytest.mark.parametrize('img_bytes,bit,in_data,out_data', [
    # Plain image, store nothing, read back LSB values
    ((0b00000000, 0b00000010, 0b00001000,
      0b00010000, 0b00010010, 0b00011000,
      0b01000000, 0b01000010, 0b01001000), 0, b'', b'\x00\x00'),
    # Store 0x5500, check bit matrix and get LSB value
    ((0b00000000, 0b00000011, 0b00001000,
      0b00010001, 0b00010010, 0b00011001,
      0b01000000, 0b01000011, 0b01001000), 0, b'\x55\x00', b'\x55\x00'),
    # Store 0x5500 in second least significant bit and check
    ((0b00000000, 0b00000010, 0b00001000,
      0b00010010, 0b00010000, 0b00011010,
      0b01000000, 0b01000010, 0b01001000), 1, b'\x55\x00', b'\x55\x00'),
    # Store 0x5580 in MSB and check
    ((0b00000000, 0b10000010, 0b00001000,
      0b10010000, 0b00010010, 0b10011000,
      0b01000000, 0b11000010, 0b11001000), 7, b'\x55\x80', b'\x55\x80'),
])
def test_img_steganography(img_bytes, bit, in_data, out_data):
    # Build a "template" 3x3 image
    s1 = (0b0000, 0b0001, 0b0100)
    s2 = (0b0000, 0b0010, 0b1000)
    image_data = bytes(a * 0x10 + b for a, b in product(s1, s2))
    img = Image.frombytes('L', (len(s1), len(s2)), image_data)

    writer = tools.make_ith_bit_writer(bit)
    reader = tools.make_ith_bit_reader(bit)

    # Write data in image
    steg_img = tools.write_to_image_bit(img, in_data, writer)
    # Check that bytes in image are what we expect
    assert tuple(steg_img.tobytes()) == img_bytes
    # Read back data and check
    assert tools.read_from_image_bit(steg_img, reader) == out_data
