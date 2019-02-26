"""This module contains (en|de)cryption tools for the game."""


def caesar(s: str, n: int) -> str:
    """Rotate the alphabet used in a string by a given amount n.
    
    The alphabet being rotated is the 26 letters English alphabet.
    n will be taken in modulo 26.
    Any character that is outside the range [a-zA-Z] is left unchanged.
    """

    n = n % 26
    a = ''.join(map(chr, range(ord('a'), ord('z')+1)))
    A = ''.join(map(chr, range(ord('A'), ord('Z')+1)))
    t = str.maketrans(a + A, a[n:] + a[:n] + A[n:] + A[:n])
    return s.translate(t)


def rot13(s: str):
    """Rotate the alphabet of a string by 13."""
    return caesar(s, 13)


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
