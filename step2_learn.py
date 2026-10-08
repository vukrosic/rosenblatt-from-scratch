"""Step 2. The 1958 demonstration, rebuilt. Cards marked on the left or on the right go in one at a time.
All 400 weights start at zero. The machine guesses, is told the answer, and changes its weights only when it was wrong."""
import random
from perc import N, SIDE, card, lit, fire_lit, teach, show
from save import save

rng = random.Random(1958)
test_rng = random.Random(7)
TEST = [(lit(x), side) for x, side in (card(test_rng) for _ in range(2000))]


def score(w, b):
    return sum(fire_lit(w, b, on) == side for on, side in TEST)


w, b = [0] * N, 0
mistakes, first, marks, snaps = [], [], {}, {}
CHECK = [0, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
marks[0] = score(w, b)
snaps[0] = w[:]
for t in range(1, 10001):
    x, side = card(rng)
    on = lit(x)
    guess = fire_lit(w, b, on)
    b, miss = teach(w, b, on, side)
    if miss:
        mistakes.append(t)
    if t <= 12:
        first.append({'t': t, 'col': on[0] % SIDE, 'row': on[0] // SIDE, 'side': side, 'guess': guess, 'miss': miss})
    if t in CHECK:
        marks[t] = score(w, b)
        snaps[t] = w[:]

print('Cards one at a time. Left = 0, right = 1. All %d weights start at zero.' % N)
for f in first:
    print('   card %2d: mark on the %-5s  guess %-5s  %s' % (f['t'], 'right' if f['side'] else 'left',
                                                           'right' if f['guess'] else 'left', 'WRONG, weights change' if f['miss'] else 'right'))
print('2,000 fresh cards, how many it gets right:')
for t in CHECK:
    print('   after %4d cards: %4d of 2,000' % (t, marks[t]))
in50 = sum(1 for m in mistakes if m <= 50)
print('Mistakes in the first 50 cards: %d. In all 10,000 cards: %d. The last mistake was on card %d.' % (in50, len(mistakes), mistakes[-1]))
print('The weights after 10,000 cards, by column (sum of the 20 squares in each column):')
cols = [sum(w[r * SIDE + c] for r in range(SIDE)) for c in range(SIDE)]
print('   ' + ' '.join('%d' % c for c in cols))
print('   left half: %d of 200 weights below zero. right half: %d of 200 above zero.' % (
    sum(1 for i in range(N) if i % SIDE < 10 and w[i] < 0), sum(1 for i in range(N) if i % SIDE >= 10 and w[i] > 0)))

save(2, first=first, marks=[[t, marks[t]] for t in CHECK], mistakes=mistakes, in50=in50, last=mistakes[-1],
     snaps=[[t, snaps[t]] for t in CHECK], final=w, bias=b, cols=cols)
