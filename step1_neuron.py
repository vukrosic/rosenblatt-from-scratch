"""Step 1. The model nerve cell of 1943: inputs vote, each with a weight, and the cell answers yes above a threshold.
Here every weight is set by hand. Nothing learns yet."""
import random
from perc import N, SIDE, fire, card, lit, fire_lit
from save import save

# Take an umbrella? Three yes/no facts vote. The weights say how much each fact counts.
FACTS = ['dark clouds', 'forecast says rain', 'going by car']
W, B = [2, 3, -4], -2   # answer yes if 2*clouds + 3*forecast - 4*car is above 2
print('Take an umbrella?  weights: clouds +2, forecast +3, car -4. Yes if the sum is above 2.')
umbrella = []
for n in range(8):
    x = [(n >> 2) & 1, (n >> 1) & 1, n & 1]
    total = sum(w * v for w, v in zip(W, x))
    yes = fire(W, B, x)
    umbrella.append({'x': x, 'sum': total, 'yes': yes})
    print('   clouds %d  forecast %d  car %d   sum %2d   %s' % (x[0], x[1], x[2], total, 'yes' if yes else 'no'))

# Two switches and a lamp. Each rule is one cell with hand-set weights.
RULES = {'both (AND)': ([1, 1], -1), 'at least one (OR)': ([1, 1], 0), 'not the first (NOT)': ([-1, 0], 1)}
tables = {}
for name, (w, b) in RULES.items():
    out = [fire(w, b, [p, q]) for p in (0, 1) for q in (0, 1)]
    tables[name] = {'w': w, 'b': b, 'out': out}
    print('%-20s weights %s, bias %2d   answers for 00 01 10 11: %s' % (name, w, b, ' '.join(map(str, out))))

# A card with a mark on the left or on the right. By hand: -1 on the 200 left squares, +1 on the 200 right squares.
hand = [1 if i % SIDE >= SIDE // 2 else -1 for i in range(N)]
rng = random.Random(1)
right = 0
for _ in range(1000):
    x, side = card(rng)
    right += fire_lit(hand, 0, lit(x)) == side
print('Left or right mark, %d weights set by hand: %d of 1,000 cards right.' % (N, right))
print('That took %d numbers, and we knew the answer in advance. For the letter X against the letter E, nobody knows the %d numbers.' % (N, N))

save(1, umbrella=umbrella, facts=FACTS, w=W, b=B, tables=tables, hand_right=right, n=N)
