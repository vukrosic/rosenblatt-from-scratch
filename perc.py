"""The perceptron and the pictures it looks at. Plain Python, nothing to install."""
import random

SIDE = 20            # the Mark I looked through 20 by 20 photocells
N = SIDE * SIDE      # 400 squares


def fire(w, b, x):
    """One model nerve cell. Every input votes with its weight. Answer 1 if the votes add up above zero."""
    return 1 if sum(wi * xi for wi, xi in zip(w, x)) + b > 0 else 0


def lit(x):
    """The squares that are on. A dark square votes with zero, so only these matter."""
    return [i for i, v in enumerate(x) if v]


def fire_lit(w, b, on):
    s = b
    for i in on:
        s += w[i]
    return 1 if s > 0 else 0


def teach(w, b, on, want):
    """Rosenblatt's rule. Right answer: change nothing.
    Wrong answer: add the input to the weights (if it should have said yes) or take it away (if no).
    Returns the new bias and 1 if this was a mistake."""
    if fire_lit(w, b, on) == want:
        return b, 0
    step = 1 if want == 1 else -1
    for i in on:
        w[i] += step
    return b + step, 1


# ---- pictures on the 20 by 20 retina ----

def blank():
    return [0] * N


def card(rng):
    """A punch card with one 4 by 4 mark, on the left half or on the right half. Returns (picture, side); side 1 = right."""
    side = rng.randrange(2)
    col = rng.randrange(0, 7) + (10 if side else 0)
    row = rng.randrange(0, 17)
    x = blank()
    for r in range(row, row + 4):
        for c in range(col, col + 4):
            x[r * SIDE + c] = 1
    return x, side


G = 12  # letters are drawn 12 by 12


def _glyph(name):
    g = [[0] * G for _ in range(G)]
    for i in range(G):
        for j in range(G):
            if name == 'X':
                on = abs(i - j) <= 1 or abs(i + j - (G - 1)) <= 1
            elif name == 'E':
                on = j <= 1 or (i <= 1 or i >= G - 2 or i in (5, 6)) and j <= G - 2
            elif name == 'T':
                on = i <= 1 or j in (5, 6)
            else:  # 'O'
                on = (i <= 1 or i >= G - 2 or j <= 1 or j >= G - 1 - 1) and not ((i in (0, G - 1)) and (j in (0, G - 1)))
            g[i][j] = 1 if on else 0
    return g


LETTERS = ['X', 'E', 'T', 'O']
GLYPH = {name: _glyph(name) for name in LETTERS}


def letter(name, rng, noise=6):
    """The letter at a random place on the retina, with a few squares flipped."""
    dy, dx = rng.randrange(0, SIDE - G + 1), rng.randrange(0, SIDE - G + 1)
    x = blank()
    g = GLYPH[name]
    for i in range(G):
        for j in range(G):
            if g[i][j]:
                x[(i + dy) * SIDE + j + dx] = 1
    for i in rng.sample(range(N), noise):
        x[i] = 1 - x[i]
    return x


def letter_set(seed, count):
    """`count` letters in mixed order, as (picture, number of the letter)."""
    rng = random.Random(seed)
    out = [(letter(LETTERS[k % len(LETTERS)], rng), k % len(LETTERS)) for k in range(count)]
    rng.shuffle(out)
    return out


def show(x, side=SIDE):
    return '\n'.join(''.join('#' if x[r * side + c] else '.' for c in range(side)) for r in range(side))
