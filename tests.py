"""Checks. run_all.sh runs them last, on the numbers the seven steps saved in runs/, and on the cell itself."""
import json
import os
import random
from perc import N, SIDE, LETTERS, fire, fire_lit, teach, card, lit, letter_set

HERE = os.path.dirname(os.path.abspath(__file__))
r = {i: json.load(open(os.path.join(HERE, 'runs', 'step%d.json' % i))) for i in range(1, 8)}

# the cell: a weighted vote against zero; the two ways of asking it agree
rng = random.Random(0)
for _ in range(200):
    w = [rng.randint(-3, 3) for _ in range(N)]
    x, _ = card(rng)
    assert fire(w, 1, x) == fire_lit(w, 1, lit(x))
# the rule: a right answer changes nothing, a wrong answer moves only the lit squares, by one
w = [0] * N
x, side = card(random.Random(5))
on = lit(x)
b, miss = teach(w, 0, on, 1)
assert miss == 1 and b == 1 and sum(w) == len(on) == 16 and all(w[i] == 1 for i in on)
before = w[:]
assert teach(w, b, on, 1) == (b, 0) and w == before
# the letter sets: a quarter each, and the test letters are not the training letters
train, test = letter_set(3, 2000), letter_set(4, 1000)
assert [sum(1 for _, k in test if k == j) for j in range(4)] == [250] * 4 and len(LETTERS) == 4
assert not {tuple(x) for x, _ in test} & {tuple(x) for x, _ in train}

# 1. the umbrella cell says yes in 2 of 8 cases; the hand-set weights sort every card
assert sum(u['yes'] for u in r[1]['umbrella']) == 2 and r[1]['hand_right'] == 1000
assert r[1]['tables']['both (AND)']['out'] == [0, 0, 0, 1] and r[1]['tables']['at least one (OR)']['out'] == [0, 1, 1, 1]

# 2. learning from mistakes: from a coin flip to every fresh card right, and the mistakes stop
marks = dict(r[2]['marks'])
assert marks[0] < 1100 and marks[50] > 1900 and marks[1000] == 2000
assert r[2]['in50'] == sum(1 for m in r[2]['mistakes'] if m <= 50) and r[2]['last'] == r[2]['mistakes'][-1] < 1000
assert sum(r[2]['cols'][:10]) < 0 < sum(r[2]['cols'][10:]) and len(r[2]['final']) == N and SIDE == 20

# 3. the Mark I: 512 fixed random middle units, 2,048 knobs, far above chance on letters it never saw
assert r[3]['a_units'] == 512 and r[3]['knobs'] == 2048 and r[3]['history'][0][1] <= 300 and r[3]['right'] > 950
assert sum(p[0] for p in r[3]['per']) == r[3]['right'] and all(p[1] == 250 for p in r[3]['per'])

# 4. the guarantee: it stopped on all 1,000 problems, and never passed the ceiling
assert r[4]['total'] == 1000 and r[4]['worst'] <= 1
assert all(row['high'] <= row['ceiling'] for row in r[4]['rows']) and r[4]['example']['mistakes'] <= r[4]['example']['ceiling']
avgs = [row['avg'] for row in r[4]['rows']]
assert avgs == sorted(avgs)                      # a narrower gap costs more mistakes

# 5. the stairway lamp: no cell does it, the rule never settles; 14 of the 16 two-switch rules are possible
assert r[5]['best'] == 3 and r[5]['counts']['xor'] == 0 and r[5]['can'] == 14
assert sorted(r[5]['missing']) == [[0, 1, 1, 0], [1, 0, 0, 1]] and r[5]['changes'] > 100000
par = {p['k']: p for p in r[5]['parity']}
assert par[9]['best'] == 512 and par[9]['units'] == 512 and par[8]['best'] < 512 and par[1]['best'] < 400

# 6. three cells by hand do the lamp; random middle cells need about one cell per case
assert [h['out'] for h in r[6]['hand']] == [0, 1, 1, 0]
need = {x['n']: x['cells'] for x in r[6]['need']}
assert need[2] <= 32 and need[8] >= 128 and all(need[n] <= need[n + 1] for n in range(2, 8))

# 7. blame passed backward: the middle cells learn, and a few of them beat 512 random ones
assert r[7]['lamp_solved'] > 50 and r[7]['lamp4'] == 100
assert all(o['solved'] >= 5 and o['cells'] < o['random'] for o in r[7]['odd'])
assert all(x['right'] > r[7]['mark1'] and x['cells'] < 512 for x in r[7]['letters'])
last = r[7]['trace'][-1]['outs']
assert last[0] < 0.5 < last[1] and last[3] < 0.5 < last[2]

print('All checks passed.')
