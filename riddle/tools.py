"""This module contains (en|de)cryption tools for the game."""

# import numpy as np
from PIL import Image
from textwrap import dedent


def _get_alphabets(alphabet):
    if callable(alphabet):
        a = alphabet()
    else:
        a = (alphabet,)
    l = len(a[0])
    # Ensure all alphabets have the same length
    assert all(len(s) == l for s in a)
    return a, l


def e26_alphabet():
    """26 characters English alphabets, lower and upper cases."""
    a = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
    A = ''.join(map(chr, range(ord('A'), ord('Z') + 1)))
    # We return 2 equivalent alphabet
    return a, A


def sym_alphabet():
    """Common symbols, number and English letter alphabet."""
    s = '.,:;<>()[]{}\'"`-_=+*/%\\'
    n = '0123456789'
    l = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
    u = ''.join(map(chr, range(ord('A'), ord('Z') + 1)))
    # We return a single alphabet
    return (n + l + u + s,)


def caesar(s: str, n: int, alphabet=e26_alphabet) -> str:
    """Rotate the alphabet used in a string by a given amount n.
    
    By default, the alphabet being rotated is the 26 letters
    English alphabet.
    n will be taken in modulo len(alphabet).
    Any character that is outside the alphabet is left unchanged.

    The parameter alphabet can be used to specify a different
    alphabet. It must be a single string or a callable returning
    a tuple of strings containing one or more alphabet with
    same length.
    """

    a, l = _get_alphabets(alphabet)
    # Ensure n is in a valid range
    n = n % l
    # Unrotated version of each alphabet
    u = ''.join(a)
    # Rotated version of each alphabet
    r = ''.join([s[n:] + s[:n] for s in a])
    t = str.maketrans(u, r)
    # t = str.maketrans(a + A, a[n:] + a[:n] + A[n:] + A[:n])
    return s.translate(t)


def rot13(s: str):
    """Rotate the alphabet of a string by 13."""
    return caesar(s, 13, e26_alphabet)


def vigenere(s: str, k: str, alphabet=e26_alphabet) -> str:
    """Compute the Vigenère cipher for a string s with key k."""
    return s


def ca1D_step(l: '[0,1,0,1] or "0101"', rule: range(256), boundary) -> list:
    """Perform one step of 1D cellular automata according to the given rule.
    
    l: the initial state of the 1D automata, as a list of bits.
    rule: a number from 0 to 255 that encodes the transition rule.
    boundary: loop, extend, even (1,0), odd (0,1), 1 or 0 (default)

    Since the automata is 1D, each cell has normally two neighbors, that is,
    each cell has a binary state and its future state depends on 2 other bits.
    All the possible states for a cell can be represented by 8 combinations:
        000, 001, 010, 011, 100, 101, 110, 111
    e.g. in 010, the cell has value 1 and its neighbors have value 0,0
         in 110, the cell has value 1 and only its left neighbor has value 1

    Rules are expressed as 8 bits, i.e. 2^8 = 256 combinations are possible.
    Each bit in the rule, represents the outcome of a possible input. Since
    there are 8 possible inputs, like the rule size, each bit of the rule
    determines the output of each of the 8 possible inputs.

    Example, the rule 30 (00011110) will imply this transition table:
     000 -> 0
     001 -> 0
     010 -> 0
     011 -> 1
     100 -> 1
     101 -> 1
     110 -> 1
     111 -> 0

    So, if the automata is in state [0,1,1,0,0,0] and we assume boundary is 0
    we get:
     0|01  -> 0
      011  -> 1
      110  -> 1
      100  -> 1
      000  -> 0
      00|0 -> 0
    therefore ca1_step([0,1,1,0,0,0], 30, boundary=0) == [0,1,1,1,0,0]
    """
    assert rule in range(256)

    # Ensure the list is binary
    if isinstance(l, str):
        return_str = True
        l = [0 if c == '0' else 1 for c in l]
    else:
        return_str = False
        l = [1 if c else 0 for c in l]

    print("Got input list", l)

    # Resolve boundary first
    if boundary == 'loop':
        l = l[-1:] + l + l[:1]
    elif boundary == 'extend':
        l = l[:1] + l + l[-1:]
    elif boundary == 'even':
        l = [1] + l + [0]
    elif boundary == 'odd':
        l = [0] + l + [1]
    elif boundary == 1 or boundary == '1' or boundary == 'one':
        l = [1] + l + [1]
    elif boundary == 0 or boundary == '0' or boundary == 'zero':
        l = [0] + l + [0]
    else:
        raise ValueError(f"Invalid boundary value '{boundary}'")

    # Convert the rule for easier access
    rule = list(map(int, bin(rule)[2:]))
    rule = [0] * (8 - len(rule)) + rule
    # print("Rule being used", rule)

    # Apply the rule
    print("Iterating list", l)
    out_state = []
    for i, c in enumerate(l[1:-1], 1):
        s = 4 * l[i-1] + 2 * c + l[i+1]  # State of cell and heighbors
        out_state.append(rule[s])

    print("Output state is", out_state)
    if return_str:
        return ''.join(map(str, out_state))
    return out_state


def cantor_generate():
    """Generate positions in grid according to Cantor's enumeration."""
    p = (0, 0)  # Starting position
    d = 1  # direction (increment or decrement)
    while True:
        yield p
        if d == 1 and p[0] == 0:
            d = -1
            p = p[0], p[1] + 1
        elif d == -1 and p[1] == 0:
            d = 1
            p = p[0] + 1, p[1]
        else:
            p = p[0] - d, p[1] + d


def cantor_position(n):
    """Return n-th cantor position."""
    r = int(1 + (1 + 8 * n) ** 0.5) // 2 - 1
    c = n - r * (r + 1) // 2
    if r % 2 == 0:
        return r - c, c
    return c, r - c


def dumb_primality_test(n):
    """Return True if n is prime, False otherwise."""
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(n):
    """Return the list of primes not greater of n."""
    primes = [True] * n
    i, sqrtn = 2, n ** 0.5
    while i < sqrtn:
        if primes[i]:
            for j in range(i * i, n, i):
                primes[j] = False
        i += 1
    return [i for i, v in enumerate(primes[2:], 2) if v]


def prime_generator():
    """Generate prime numbers forever and ever until your computer explodes."""
    p = 2
    yield p
    while True:
        p += 1
        if dumb_primality_test(p):  # SLOW!
            yield p


def bits_to_tuple(b, n):
    """Convert the number into a tuple with given size."""
    assert b in range(2 ** n)
    v = []
    for i in range(n):
        v.insert(0, b >> i & 1)
    return tuple(v)


def tuple_to_bits(b):
    """Convert a tuple of bits to a number."""
    return sum(d << i for i, d in enumerate(reversed(b)))


def bit3_to_rgb(b):
    return tuple(i * 0xff for i in bits_to_tuple(b, 3))


def draw_subpixel_text(s: str):
    # Encoding found here: http://www.msarnoff.org/millitext/
    encodings3 = {
        '0': '75557', '1': '62227', '2': '71747', '3': '71717', '4': '74717',
        '5': '74757', '6': '74757', '7': '75111', '8': '75757', '9': '75717',
        'A': '75755', 'B': '65656', 'C': '74447', 'D': '65556', 'E': '74747',
        'F': '74744', 'G': '74557', 'H': '55755', 'I': '72227', 'J': '11117',
        'K': '55655', 'L': '44447', 'M': '57755', 'N': '65555', 'O': '25552',
        'P': '65644', 'Q': '25573', 'R': '65655', 'S': '34216', 'T': '72222',
        'U': '55557', 'V': '55531', 'W': '55775', 'X': '55255', 'Y': '55111',
        'Z': '71247', ' ': '00000', '.': '00033', "'": '22000', '"': '33000',
        '!': '34404', '?': '31202',
        ',': '000012',
    }

    def _tupleize(c):
        return map(bit3_to_rgb, map(int, encodings3.get(c.upper(), '')))

    def _render(text, surface):
        for i, c in enumerate(text):
            rows = _tupleize(c)
            for j, row in enumerate(_tupleize(c)):
                surface.putpixel((i*2, j), row)
            # draw_on_image(rows, x=some_shift)

    rows = []
    max_w = 0
    for line in s.split('\n'):
        w = len(line) * 2
        max_w = max(w, max_w)
        # Each row is 6 pixels tall (5+margin) and wide 1px per letter + margin
        row = Image.new('RGB', (w, 6))
        _render(line, row)
        rows.append(row)

    # Compose the rows stacking them vertically
    full = Image.new('RGB', (max_w + 1, 7 * len(rows)))
    for i, row in enumerate(rows):
        full.paste(row, (1, i * 7))
    return full


def generate_bits(data: bytes):
    """Yield the bits into data, one at time, followed by infinite zeros"""
    for n in data:
        yield from (b for b in bits_to_tuple(n, 8))
    while True:
        yield 0


def lsb_writer(byte, bit):
    return byte & 0b11111110 | bit


def lsb_reader(byte):
    return byte & 0b00000001


def make_ith_bit_writer(i):
    def _writer(byte, bit):
        return byte & (0xff - (1 << i)) | bit << i
    return _writer


def make_ith_bit_reader(i):
    def _reader(byte):
        return (byte & (1 << i)) >> i
    return _reader


def write_to_image_bit(img, data: bytes, bit_writer=lsb_writer):
    """Write to image the binary data, one bit at time, with zero padded tail.
    This function does NOT check for lengths and will NOT raise errors; it is
    caller's responsibility to ensure the message fits the image.
    """
    buff = bytearray()
    for p, d in zip(img.tobytes(), generate_bits(data)):
        buff.append(bit_writer(p, d))
    return Image.frombytes(img.mode, img.size, bytes(buff))


def read_from_image_bit(img, bit_reader=lsb_reader):
    """Read data written using write_to_image_lsb."""
    data = []
    datum = []
    for p in img.tobytes():
        datum.append(bit_reader(p))
        if len(datum) == 8:
            data.append(tuple_to_bits(datum))
            datum.clear()
    # Do not discard partial bits
    while len(datum) < 8:
        datum.append(0)
    data.append(tuple_to_bits(datum))
    return bytes(data)


if __name__ == '__main__':
    text = dedent('''\
        "The quick brown fox jumps over the lazy dog"
        is a typical sentence used to test fonts as it contains all the 26
        English letters, but in our case, we need to test "points" as well!
        What d'ya think?''')
    draw_subpixel_text(text).save('prova.png')

    msb_writer = make_ith_bit_writer(5)
    msb_reader = make_ith_bit_reader(5)

    img = Image.open("../demo_image.jpg")
    img2 = write_to_image_bit(img, 'Hello there! ☺'.encode(), msb_writer)
    img2.show()
    print(read_from_image_bit(img2, msb_reader).decode())
