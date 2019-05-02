"""This module contains (en|de)cryption tools for the game."""

# import numpy as np
import ast
import asn1
import random
import operator
import itertools
from PIL import Image
from collections import defaultdict
from textwrap import dedent
from base64 import b64encode, b64decode


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


def _sm_prime_test(n):
    if n in {0, 1, 4, 6, 8, 9, 10}:
        return False
    if n in {2, 3, 5, 7, 11}:
        return True
    if n % 2 == 0: # or n % 3 == 0 or n % 5 == 0 or n % 7 == 0:
        return False
    return None


def _p2fact(n):
    """Write n as 2^r * d + 1, d odd."""
    r, d = 0, n - 1
    while d % 2 == 0:
        d = d >> 1
        r += 1
    return r, d


def miller_primality_test(n):
    """Implement the (deterministic) Miller primality test (True if prime)."""
    t = _sm_prime_test(n)
    if t is not None:
        return t

    r, d = _p2fact(n)

    from math import floor, log

    up = floor(2 * log(n)**2)
    for a in range(2, min(n - 2, up)):
        x = pow(a, d, n)  # a ** d % n, but way more efficient
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                continue
        return False
    return True


def sieve_of_eratosthenes(n):
    """Return the list of primes not greater of n.
    
    This uses arbitrarily large integers as boolean array
    and uses a wheel to skip multiples of 2, 3 and 5.
    """
    primes, start = [2, 3, 5], 7
    inc = [4, 2, 4, 2, 4, 6, 2, 6]

    table = 0
    wheel = itertools.cycle(inc)
    i, sqrtn = start, n ** 0.5
    while i < sqrtn:
        if (table >> i) & 1 == 0:
            for j in range(i * 2, n, i):
                table |= 1 << j
        i += next(wheel)

    wheel = itertools.cycle(inc)
    i = start
    while i < n:
        if (table >> i) & 1 == 0:
            primes.append(i)
        i += next(wheel)
    return primes


def _dumb_prime_generator():
    """Generate prime numbers forever and ever until your computer explodes."""
    yield from [2, 3, 5, 7]
    p = 8
    while True:
        p += 1
        if miller_primality_test(p):
            yield p


def generate_big_prime(bits, rng=None):
    """Start from random bits and decrement until a prime is found."""
    if bits <= 1:
        return None
    if rng is None:
        rng = random
    if bits == 2:
        return rng.choice([2, 3])
    n = rng.getrandbits(bits) | 1  # Ensure it's odd
    # Decrement until a prime is found
    while n > 5:
        if miller_primality_test(n):
            return n
        n -= 2


def prime_generator():
    """Generate prime numbers forever and ever until your computer explodes.
    
    This generator is way slower than the sieve_of_eratosthenes: use that one
    if you know how many primes to generate or if you have enough memory.

    This is an iterative, non-recursive version of the Melissa E. O'Neill's
        https://www.cs.hmc.edu/~oneill/papers/Sieve-JFP.pdf
    but mine is less efficient, so - as she argues - it is not the same algo.

    There are better version on line, if you care
        https://rosettacode.org/wiki/Sieve_of_Eratosthenes#Python
    """
    yield 2
    # Table of (next) multiples: each entry (key) associates the next multiple
    # to be tested with its generating prime (value)
    multiples = dict()
    # i is the candidate prime number
    for i in itertools.count(3, 2):  # Start with 3 and skip even numbers
        if i in multiples:
            # Get the prime number associated to the composite multiple i
            p = multiples[i]
            # Compute multiples of p until there is a free spot in the table
            # and ensure we don't get a multiple of skipped numbers (2, here)
            n = i + p
            while n in multiples or n % 2 == 0:
                n += p
            multiples[n] = multiples.pop(i) 
        else:
            yield i  # This number is prime, as it is not a multiple
            multiples[i * i] = i


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


class SimpleRSA:
    """This class implements a simplified RSA to encode and decode bytes."""

    def __init__(self, p, q, exp_size=8, rng=None):
        """Generate public and private keys for prime numbers p and q."""
        n = p * q  # Compute modulo
        z = (p - 1) * (q - 1)  # Euler totient function, phi(n)
        # Find a prime that does not divide z
        while True:
            k1 = generate_big_prime(exp_size, rng)
            if k1 in [p, q]:
                continue
            if z % k1 != 0:
                break

        for j in itertools.count(1):
            k2, r = divmod(j * z + 1, k1)
            if r == 0:
                break

        self.public_key = (n, k1)
        self.private_key = (n, k2)

    def encode(self, msg, key):
        """Encode a message, one byte at time."""
        n, k = key
        cry = []
        for m in msg:
            c = m ** k % n
            cry.append(c)
        return cry

    def decode(self, cry, key):
        """Decode a message, one byte at time."""
        n, k = key
        msg = bytearray()
        for c in cry:
            m = c ** k % n
            msg.append(m)
        return msg.decode()

    def serialize_key(self, key):
        """Serialize a key with ASN.1, b64 encoded."""
        encoder = asn1.Encoder()
        encoder.start()
        # Not really standard
        encoder.write(key[0], asn1.Numbers.Integer)
        encoder.write(key[1], asn1.Numbers.Integer)
        encoder = encoder.output()
        return b64encode(encoder)

    def deserialize_key(self, key):
        """Deserialize from b64 and ASN.1."""
        data = b64decode(key)
        decoder = asn1.Decoder()
        decoder.start(data)
        _, n = decoder.read()
        _, k = decoder.read()
        return (n, k)


def make_highly_variable_graph(n):
    graph = defaultdict(set)
    for i in range(n):
        for j in range(random.randint(0, n)):
            if random.random() > 0.5 and i != j:
                graph[i].add(j)
    for i in range(3):
        graph[0].add(random.randint(1, n))
    return graph


def calculate_graph_longest_path(graph):

    def calc_dfs(v, seen=None, path=None):
        if seen is None:
            seen = []
        if path is None:
            path = [v]

        seen.append(v)

        paths = []
        for t in graph[v]:
            if t not in seen:
                t_path = path + [t]
                paths.append(tuple(t_path))
                paths.extend(calc_dfs(t, seen[:], t_path))
        return paths

    return max(len(el) for el in calc_dfs(0))


def eval_expr(s, enabled_ops='pn+-*/^%'):
    """Evaluate an expression using ast.

    Credits and docs:
     - https://stackoverflow.com/a/9558001
     - https://docs.python.org/3/library/operator.html#mapping-operators-to-functions
    """
    if not s:
        return None  # Nothing to evaluate

    # Keep a table of operators that can be used
    op_table = {
        'p': (ast.UAdd, operator.pos),
        'n': (ast.USub, operator.neg),
        '+': (ast.Add, operator.add),
        '-': (ast.Sub, operator.sub),
        '*': (ast.Mult, operator.mul),
        '/': (ast.Div, operator.truediv),
        '^': (ast.Pow, operator.pow),
        '%': (ast.Mod, operator.mod),
    }

    ops = dict(op_table[o] for o in enabled_ops)

    def eval_(n):
        try:
            if isinstance(n, ast.Num):
                return n.n
            elif isinstance(n, ast.BinOp):
                return ops[type(n.op)](eval_(n.left), eval_(n.right))
            elif isinstance(n, ast.UnaryOp):
                return ops[type(n.op)](eval_(n.operand))
        except KeyError:
            raise SyntaxError('unknown token')
        raise TypeError(n)
    return eval_(ast.parse(s.strip(), mode='eval').body)


if __name__ == '__main__':
    print(sieve_of_eratosthenes(30))
    if False:
        import time
        from operator import eq
        count = 1000000
        print("Generating primes below", count)

        start = time.time()
        table_primes = sieve_of_eratosthenes(count)
        table_time = time.time() - start
        print("  Table took", table_time, "[s]")

        start = time.time()
        gen_primes = list(p for _, p in zip(range(count), prime_generator()))
        gen_time = time.time() - start
        print("  Generator took", gen_time, "[s]")

        print("Same?", all(itertools.starmap(eq,
                                             zip(table_primes, gen_primes))))

        # This is slow, don't try it for large numbers
        if count < 10000:
            start = time.time()
            dumb_primes = list(p for _, p in zip(range(count),
                                                 _dumb_prime_generator()))
            dumb_time = time.time() - start
            print("  Dumb generator took", dumb_time, "[s]")

            print("Same?", all(itertools.starmap(eq,
                                                 zip(table_primes, dumb_primes))))

    if False:
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
        img2.save("./encoded.png")
        print(read_from_image_bit(img2, msb_reader).decode())

    if False:
        rsa = SimpleRSA(13, 17)
        print("Generated keys", rsa.serialize_key(rsa.public_key),
                                rsa.serialize_key(rsa.private_key))

    if True:
        text = input("Insert the text you want to encode (will be stripped): ")
        text = text.strip()

        img = Image.open(input("Path for input image: "))
        img2 = write_to_image_bit(img, text.encode(), lsb_writer)
        img2.save(input("Path for output image: "))
        print(read_from_image_bit(img2, lsb_reader).decode())
