import re
import random
from pathlib import Path
from string import ascii_letters


def conv(w):
    """Map words to integers, only a-z0-9 letters are ok"""
    return ''.join(reversed(str(int(w, 36))))


def mconv(m):
    return conv(m.group())


def main():
    # Input directory
    in_dir = 'plans'

    out_dir = Path(conv(in_dir))
    out_dir.mkdir(exist_ok=True)
    for f in Path(in_dir).glob('*'):
        doc = f.open().read()
        cod = re.sub(r'[a-zA-Z0-9]+', mconv, doc)
        of = out_dir / conv(f.stem)
        of.open(mode='wt').write(cod)


if __name__ == '__main__':
    main()
