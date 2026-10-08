"""Step 4. The guarantee. If one straight line can split the two groups, the rule finds such a line,
and the number of mistakes on the way has a ceiling: (R / gap)^2. We test it on 1,000 made-up problems.
Whole numbers only, so every Python prints the same."""
import random
from save import save

SIZE = 50      # points lie on a grid from -50 to 50
ONE = 50       # the constant third input (lets the line sit away from the centre)


def problem(rng, gap, count=40):
    """Points on a grid, split by a hidden line a*x + b*y + c = 0, with nothing closer to the line than `gap`."""
    while True:
        a, b = rng.randrange(-9, 10), rng.randrange(-9, 10)
        if a or b:
            break
    c = rng.randrange(-150, 151)
    norm = (a * a + b * b) ** 0.5
    pts = []
    while len(pts) < count:
        x, y = rng.randrange(-SIZE, SIZE + 1), rng.randrange(-SIZE, SIZE + 1)
        d = a * x + b * y + c
        if abs(d) / norm >= gap:
            pts.append((x, y, 1 if d > 0 else 0))
    if len({p[2] for p in pts}) < 2:
        return problem(rng, gap, count)
    return pts, (a, b, c)


def ceiling(pts, line):
    """(R / gap)^2 for this problem, measured with the hidden line (all three inputs counted)."""
    a, b, c = line
    k = c / ONE
    norm = (a * a + b * b + k * k) ** 0.5
    margin = min(abs(a * x + b * y + c) for x, y, _ in pts) / norm
    r2 = max(x * x + y * y + ONE * ONE for x, y, _ in pts)
    return r2 / (margin * margin)


def learn(pts, rng, trace=False):
    """Rosenblatt's rule on points. Returns the mistakes, and the line after each mistake if asked."""
    w = [0, 0, 0]
    order = list(range(len(pts)))
    mistakes, lines = 0, []
    while True:
        rng.shuffle(order)
        clean = True
        for i in order:
            x, y, want = pts[i]
            got = 1 if w[0] * x + w[1] * y + w[2] * ONE > 0 else 0
            if got != want:
                s = 1 if want else -1
                w[0] += s * x
                w[1] += s * y
                w[2] += s * ONE
                mistakes += 1
                clean = False
                if trace:
                    lines.append({'w': w[:], 'i': i})
        if clean:
            return mistakes, lines, w


rng = random.Random(1962)
rows = []
total = 0
worst_share = 0.0
print('gap    problems   mistakes: fewest  average  most    ceiling on average')
for gap in (20, 10, 5, 2, 1):
    ms, cs = [], []
    for _ in range(200):
        pts, line = problem(rng, gap)
        m, _, _ = learn(pts, rng)
        c = ceiling(pts, line)
        assert m <= c
        worst_share = max(worst_share, m / c)
        ms.append(m)
        cs.append(c)
    total += len(ms)
    rows.append({'gap': gap, 'low': min(ms), 'avg': sum(ms) / len(ms), 'high': max(ms), 'ceiling': sum(cs) / len(cs)})
    print('%3d      %4d          %6d  %7.1f  %5d    %12s' % (gap, len(ms), min(ms), sum(ms) / len(ms), max(ms), format(round(sum(cs) / len(cs)), ',')))
print('%s problems. The rule stopped on every one. Closest it came to its ceiling: %.0f%% of it.' % (format(total, ','), 100 * worst_share))

# One problem to draw: the line after every mistake.
rng = random.Random(8)
while True:
    pts, line = problem(rng, 6, 30)
    m, lines, w = learn(pts, random.Random(1), trace=True)
    if 7 <= m <= 10:
        break
print('The drawn example: 30 points, gap 6, %d mistakes, ceiling %s.' % (m, format(round(ceiling(pts, line)), ',')))

save(4, rows=rows, total=total, worst=worst_share, example={'pts': pts, 'line': line, 'steps': lines, 'final': w, 'mistakes': m, 'ceiling': ceiling(pts, line)}, one=ONE, size=SIZE)
