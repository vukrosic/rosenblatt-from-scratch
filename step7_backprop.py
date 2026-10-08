"""Step 7. The rule of 1986. Each cell answers with a smooth slope instead of a hard yes or no.
Then a mistake at the end can be passed backward: every weight learns how much it was to blame.
Now the middle layer learns too."""
import random
from math import exp
from perc import N, LETTERS, letter_set, lit
from save import save


def soft(z):
    """The smooth cell: near 0 for very negative sums, near 1 for very positive ones, a slope between."""
    if z < -40:
        return 0.0
    if z > 40:
        return 1.0
    return 1.0 / (1.0 + exp(-z))


class Net:
    """Inputs -> `h` middle cells -> `outs` end cells. Inputs are given as the list of squares that are on."""

    def __init__(self, n, h, outs, rng, spread=1.0):
        self.w1 = [[rng.uniform(-spread, spread) for _ in range(n)] for _ in range(h)]
        self.b1 = [rng.uniform(-spread, spread) for _ in range(h)]
        self.w2 = [[rng.uniform(-1, 1) for _ in range(h)] for _ in range(outs)]
        self.b2 = [rng.uniform(-1, 1) for _ in range(outs)]

    def run(self, on):
        mid = [soft(b + sum(w[i] for i in on)) for w, b in zip(self.w1, self.b1)]
        out = [soft(b + sum(wj * m for wj, m in zip(w, mid))) for w, b in zip(self.w2, self.b2)]
        return mid, out

    def learn(self, on, want, rate):
        mid, out = self.run(on)
        blame_out = [o - t for o, t in zip(out, want)]                       # how wrong each end cell was
        blame_mid = [m * (1 - m) * sum(blame_out[k] * self.w2[k][j] for k in range(len(out))) for j, m in enumerate(mid)]
        for k, d in enumerate(blame_out):                                     # the end cells correct themselves
            w = self.w2[k]
            for j, m in enumerate(mid):
                w[j] -= rate * d * m
            self.b2[k] -= rate * d
        for j, d in enumerate(blame_mid):                                     # and the blame goes back to the middle
            w = self.w1[j]
            step = rate * d
            for i in on:
                w[i] -= step
            self.b1[j] -= step
        return out


def odd_even(n):
    return [([i for i in range(n) if (k >> i) & 1], [bin(k).count('1') % 2]) for k in range(1 << n)]


def train_odd(n, h, rng, passes, rate=0.5, trace=None, spread=1.0):
    data = odd_even(n)
    net = Net(n, h, 1, rng, spread=spread)
    order = list(range(len(data)))
    for p in range(1, passes + 1):
        rng.shuffle(order)
        for i in order:
            net.learn(data[i][0], data[i][1], rate)
        outs = [net.run(on)[1][0] for on, _ in data]
        ok = sum((o > 0.5) == bool(t[0]) for o, (_, t) in zip(outs, data))
        if trace is not None and (p <= 20 or p % 20 == 0):
            trace.append({'p': p, 'outs': [round(o, 4) for o in outs], 'w1': [[round(v, 3) for v in w] for w in net.w1],
                          'b1': [round(v, 3) for v in net.b1], 'ok': ok})
        if ok == len(data) and all(abs(o - t[0]) < 0.2 for o, (_, t) in zip(outs, data)):
            return p, net
    return None, net


# 1. The stairway lamp with two middle cells, all weights learned. 100 different random starts.
rng = random.Random(1986)
done = []
for _ in range(100):
    p, _ = train_odd(2, 2, rng, 3000)
    if p:
        done.append(p)
done.sort()
print('The stairway lamp, 2 middle cells, every weight learned: %d of 100 random starts solved it.' % len(done))
print('   passes through the four cases: fastest %d, middle %d, slowest %d' % (done[0], done[len(done) // 2], done[-1]))
rng4 = random.Random(4)
done4 = sum(1 for _ in range(100) if train_odd(2, 4, rng4, 3000)[0])
print('   with 4 middle cells: %d of 100.' % done4)
seed1 = 11
while True:                      # the first random start from 11 upward that reaches the answer
    trace = []
    p1, net1 = train_odd(2, 2, random.Random(seed1), 3000, trace=trace)
    if p1:
        break
    seed1 += 1
print('   one run in detail: solved after %d passes. Lamp guesses for 00 01 10 11 at the end: %s' % (
    p1, ' '.join('%.2f' % net1.run(on)[1][0] for on, _ in odd_even(2))))
print('   its two middle cells answer for 00 01 10 11: %s  and  %s' % tuple(
    ' '.join('%.2f' % net1.run(on)[0][j] for on, _ in odd_even(2)) for j in range(2)))

# 2. Odd or even with more switches. Twice as many middle cells as switches, 10 random starts each.
#    The starting weights are spread wider here (-3 to 3), the same spread the random cells of step 6 had.
print('Odd or even, trained middle cells (10 starts each)   against random middle cells from step 6:')
RANDOM_NEED = {2: 32, 3: 32, 4: 64, 5: 64, 6: 128, 7: 128, 8: 256}
odd = []
for n in range(2, 7):
    r = random.Random(100 + n)
    ps = [train_odd(n, 2 * n, r, 2000, rate=0.5, spread=3.0)[0] for _ in range(10)]
    ok = sorted(p for p in ps if p)
    odd.append({'n': n, 'cells': 2 * n, 'solved': len(ok), 'random': RANDOM_NEED[n], 'mid': ok[len(ok) // 2] if ok else None})
    print('   %d switches: %2d trained cells, solved in %2d of 10 starts.   Random cells needed: %d' % (n, 2 * n, len(ok), RANDOM_NEED[n]))

# 3. The letters of step 3. The Mark I had 512 random middle cells. Here a small middle layer learns.
train = [(lit(x), k) for x, k in letter_set(3, 2000)]
test = [(lit(x), k) for x, k in letter_set(4, 1000)]
letters = []
for h in (4, 16):
    net = Net(N, h, len(LETTERS), random.Random(h), spread=0.1)
    hist = []
    for p in range(1, 11):
        for on, k in train:
            net.learn(on, [1 if j == k else 0 for j in range(len(LETTERS))], 0.05)
        right = 0
        for on, k in test:
            out = net.run(on)[1]
            right += out.index(max(out)) == k
        hist.append(right)
    letters.append({'cells': h, 'history': hist, 'right': hist[-1], 'weights': h * (N + 1) + len(LETTERS) * (h + 1)})
    print('Letters, %2d trained middle cells: %d of 1,000 new letters right after 10 passes  (pass by pass: %s)' % (h, hist[-1], ' '.join(map(str, hist))))
print('The Mark I of step 3, 512 random middle cells: 976 of 1,000.')

save(7, lamp_solved=len(done), lamp_fast=done[0], lamp_mid=done[len(done) // 2], lamp_slow=done[-1], lamp4=done4,
     trace=trace, trace_passes=p1, trace_seed=seed1, odd=odd, letters=letters, mark1=976)
