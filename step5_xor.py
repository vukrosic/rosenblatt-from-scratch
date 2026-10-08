"""Step 5. The puzzle of 1969. A stairway lamp has a switch at the bottom and one at the top.
The lamp is on when exactly one switch is up. One cell with two inputs cannot learn that rule.
Then the larger version from the book: is the number of lit squares odd?"""
import random
from itertools import combinations
from operator import mul
from perc import fire
from save import save

CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
LAMP = [0, 1, 1, 0]       # on when exactly one switch is up

# 1. Rosenblatt's rule, a million cards.
rng = random.Random(1969)
w, b = [0, 0], 0
best, seen, changes = 0, set(), 0
for t in range(1000000):
    k = rng.randrange(4)
    x, want = CASES[k], LAMP[k]
    got = fire(w, b, x)
    if got != want:
        s = 1 if want else -1
        w[0] += s * x[0]
        w[1] += s * x[1]
        b += s
        changes += 1
    seen.add((w[0], w[1], b))
    best = max(best, sum(fire(w, b, c) == l for c, l in zip(CASES, LAMP)))
print('The stairway lamp, 1,000,000 cards: the weights changed %s times and never settled.' % format(changes, ','))
print('   most cases right at any moment: %d of 4. Different settings of the three numbers it visited: %d.' % (best, len(seen)))

# 2. Every cell with whole-number weights from -10 to 10: which of the 16 two-switch rules can a cell do?
rules = {}
tried = 0
for w0 in range(-10, 11):
    for w1 in range(-10, 11):
        for bias in range(-10, 11):
            tried += 1
            out = tuple(fire([w0, w1], bias, c) for c in CASES)
            rules[out] = rules.get(out, 0) + 1
missing = [r for r in ([(n >> 3) & 1, (n >> 2) & 1, (n >> 1) & 1, n & 1] for n in range(16)) if tuple(r) not in rules]
print('%s cells tried. Of the 16 possible rules for two switches, a single cell can do %d.' % (format(tried, ','), len(rules)))
print('   the missing ones (answers for 00 01 10 11): %s' % '  '.join(' '.join(map(str, m)) for m in missing))
print('   cells that do AND: %d, OR: %d, the stairway lamp: %d' % (rules[(0, 0, 0, 1)], rules[(0, 1, 1, 1)], rules.get((0, 1, 1, 0), 0)))

# 3. Odd or even? A 3 by 3 retina, all 512 pictures. The machine gets every middle unit that looks at up to k squares.
#    (A unit that looks at a set of squares is written here as the product of those squares, with dark = -1, lit = +1.
#     Any rule on up to k squares is a sum of such products, so this is the strongest machine of that kind.)
SQ = 9
PICS = [[1 if (n >> i) & 1 else -1 for i in range(SQ)] for n in range(1 << SQ)]
ODD = [1 if bin(n).count('1') % 2 else -1 for n in range(1 << SQ)]
parity = []
print('Odd or even number of lit squares, 9 squares, 512 pictures, 300 passes each:')
print('   a unit may look at    middle units    best the machine reached')
for k in range(1, SQ + 1):
    sets = [s for size in range(0, k + 1) for s in combinations(range(SQ), size)]
    feats = []
    for p in PICS:
        row = []
        for s in sets:
            v = 1
            for i in s:
                v *= p[i]
            row.append(v)
        feats.append(row)
    wk = [0] * len(sets)
    top = 0
    order = list(range(len(PICS)))
    prng = random.Random(k)
    for sweep in range(300):
        prng.shuffle(order)
        for i in order:
            f = feats[i]
            if (1 if sum(map(mul, wk, f)) > 0 else -1) != ODD[i]:
                for j, v in enumerate(f):
                    wk[j] += ODD[i] * v
        ok = sum((1 if sum(map(mul, wk, f)) > 0 else -1) == o for f, o in zip(feats, ODD))
        top = max(top, ok)
        if ok == len(PICS):
            break
    parity.append({'k': k, 'units': len(sets), 'best': top, 'sweeps': sweep + 1})
    print('   %d square%s            %4d            %3d of 512%s' % (k, ' ' if k == 1 else 's', len(sets), top, '   (after %d passes)' % (sweep + 1) if top == 512 else ''))

save(5, changes=changes, best=best, visited=len(seen), tried=tried, can=len(rules), missing=missing,
     counts={'and': rules[(0, 0, 0, 1)], 'or': rules[(0, 1, 1, 1)], 'xor': rules.get((0, 1, 1, 0), 0)}, parity=parity)
