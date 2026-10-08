"""Step 6. Two layers. Set by hand, three cells do the stairway lamp.
Then Rosenblatt's own way out: a middle layer wired at random, with only the last cell learning.
It works, and the number of random middle cells it needs explodes."""
import random
from perc import fire
from save import save

CASES = [(0, 0), (0, 1), (1, 0), (1, 1)]
LAMP = [0, 1, 1, 0]

# 1. By hand: cell A = "at least one switch is up", cell B = "both are up", last cell = "A and not B".
A, B, OUT = ([1, 1], 0), ([1, 1], -1), ([1, -1], 0)
hand = []
print('Three cells set by hand:   switches   A (at least one)   B (both)   lamp')
for x in CASES:
    a, b2 = fire(A[0], A[1], x), fire(B[0], B[1], x)
    out = fire(OUT[0], OUT[1], [a, b2])
    hand.append({'x': list(x), 'a': a, 'b': b2, 'out': out})
    print('                              %d %d            %d              %d        %d' % (x[0], x[1], a, b2, out))
assert [h['out'] for h in hand] == LAMP


# 2. Random middle layer. Each middle cell gets random whole-number weights from -3 to 3. They never change.
#    The last cell learns with Rosenblatt's rule on every case of "odd or even" for n switches.
def machine_learns(n, h, rng, sweeps=200):
    cells = [([rng.randrange(-3, 4) for _ in range(n)], rng.randrange(-3, 4)) for _ in range(h)]
    data = []
    for k in range(1 << n):
        x = [(k >> i) & 1 for i in range(n)]
        on = [j for j, (w, b) in enumerate(cells) if fire(w, b, x)]
        data.append((on, sum(x) % 2))
    w, b = [0] * h, 0
    order = list(range(len(data)))
    for _ in range(sweeps):
        rng.shuffle(order)
        clean = True
        for i in order:
            on, want = data[i]
            got = 1 if b + sum(w[j] for j in on) > 0 else 0
            if got != want:
                s = 1 if want else -1
                for j in on:
                    w[j] += s
                b += s
                clean = False
        if clean:
            return True
    return False


MACHINES = 20
SIZES = [2, 4, 8, 16, 32, 64, 128, 256, 512]
rng = random.Random(1961)
table, need = [], []
print('Random middle cells, last cell learns. Machines out of %d that got every case right:' % MACHINES)
print('switches  cases   middle cells: ' + ''.join('%5d' % h for h in SIZES))
for n in range(2, 9):
    row, found, solved = [], None, False
    for h in SIZES:
        if solved:
            row.append(None)        # already solved with fewer cells
            continue
        ok = sum(machine_learns(n, h, rng) for _ in range(MACHINES))
        row.append(ok)
        if found is None and ok >= MACHINES - 2:
            found = h
        solved = ok == MACHINES
    table.append({'n': n, 'cases': 1 << n, 'row': row})
    need.append({'n': n, 'cells': found})
    print('   %d      %4d                 ' % (n, 1 << n) + ''.join('    -' if v is None else '%5d' % v for v in row))
print('Middle cells needed for 18 of 20 machines: ' + ', '.join('%d switches: %s' % (r['n'], r['cells'] if r['cells'] else 'more than %d' % SIZES[-1]) for r in need))

save(6, hand=hand, table=table, need=need, sizes=SIZES, machines=MACHINES)
