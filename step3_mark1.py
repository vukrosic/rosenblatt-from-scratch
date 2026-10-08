"""Step 3. The Mark I Perceptron of 1960, rebuilt in numbers: 400 photocells, 512 middle units wired at random,
and response units whose weights are the only thing that learns. Task: name the letter (X, E, T or O), wherever it sits."""
import random
from perc import N, LETTERS, letter_set, show
from save import save

A_UNITS = 512
PLUS, MINUS, THRESHOLD = 10, 10, 2   # our choice: each middle unit has 10 "yes" wires and 10 "no" wires to random photocells

wire_rng = random.Random(1960)
WIRES = []
for _ in range(A_UNITS):
    cells = wire_rng.sample(range(N), PLUS + MINUS)
    WIRES.append((cells[:PLUS], cells[PLUS:]))


def middle(x):
    """Which of the 512 middle units fire for this picture. Their wires never change."""
    on = []
    for a, (plus, minus) in enumerate(WIRES):
        if sum(x[i] for i in plus) - sum(x[i] for i in minus) >= THRESHOLD:
            on.append(a)
    return on


train = [(middle(x), k, x) for x, k in letter_set(3, 2000)]
test = [(middle(x), k, x) for x, k in letter_set(4, 1000)]

# One response unit per letter. Each has 512 knobs (weights), all at zero.
W = [[0] * A_UNITS for _ in LETTERS]
B = [0] * len(LETTERS)


def sums(on):
    return [B[r] + sum(W[r][a] for a in on) for r in range(len(LETTERS))]


def answer(on):
    s = sums(on)
    return s.index(max(s))


def right(data):
    return sum(answer(on) == want for on, want, _ in data)


turns, history = 0, [[0, right(test)]]
seen = 0
for sweep in range(1, 11):
    wrong = 0
    for on, want, _ in train:
        seen += 1
        s = sums(on)
        for r in range(len(LETTERS)):
            yes = 1 if s[r] > 0 else 0
            target = 1 if r == want else 0
            if yes != target:           # the same rule as step 2, once per response unit
                step = 1 if target else -1
                for a in on:
                    W[r][a] += step
                B[r] += step
                turns += len(on)
                wrong += 1
        if seen in (50, 100, 200, 500, 1000):
            history.append([seen, right(test)])
    history.append([seen, right(test)])
    print('pass %d through the 2,000 training letters: %3d corrections; 1,000 new letters: %d right' % (sweep, wrong, right(test)))
    if wrong == 0:
        break

firing = sum(len(on) for on, _, _ in test) / len(test)
per = [[sum(1 for on, want, _ in test if want == k and answer(on) == k), sum(1 for _, want, _ in test if want == k)] for k in range(len(LETTERS))]
print('Photocells %d, middle units %d (each with %d random wires), response units used %d, knobs %d.' % (N, A_UNITS, PLUS + MINUS, len(LETTERS), A_UNITS * len(LETTERS)))
print('On average %.0f of the %d middle units fire for a letter.' % (firing, A_UNITS))
print('Knob turns in training: %s.' % format(turns, ','))
print('New letters right: %d of 1,000  (%s)' % (right(test), ', '.join('%s %d of %d' % (LETTERS[k], per[k][0], per[k][1]) for k in range(len(LETTERS)))))
print('Before any training: %d of 1,000.' % history[0][1])
ex = [{'name': LETTERS[want], 'x': x, 'on': on, 'got': LETTERS[answer(on)]} for on, want, x in test[:8]]
print(show(ex[0]['x']))

save(3, a_units=A_UNITS, wires=PLUS + MINUS, plus=PLUS, minus=MINUS, threshold=THRESHOLD, wiring=[[p, m] for p, m in WIRES[:40]],
     history=history, turns=turns, right=right(test), per=per, firing=firing, examples=ex, knobs=A_UNITS * len(LETTERS), letters=LETTERS)
