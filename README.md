# Rosenblatt from scratch

Code for the video **Become Frank Rosenblatt in 18 Minutes**.
In 1958 the psychologist Frank Rosenblatt showed a machine that learned from its own mistakes: nobody typed in the rule, it was only told "right" or "wrong". In 1969 a book proved that his machine cannot learn a rule as small as a stairway lamp with two switches, and the field went quiet for years. In 1986 one missing rule fixed it.
These seven small programs rebuild the machine, hit the wall, and add the missing rule. 729 lines of Python 3, standard library only, nothing to install.

```bash
./run_all.sh          # runs all seven steps, then the checks; 1 to 4 minutes; expected output is in demo-output.txt
python3 tests.py      # runs the checks again (needs the runs/ folder that the line above writes)
```

| File | Idea | What the run shows |
| --- | --- | --- |
| `perc.py` | The cell and the pictures | One model nerve cell (inputs vote with weights, answer yes above zero), the learning rule, cards of 20 by 20 squares, the letters X, E, T, O. Every step imports it. |
| `step1_neuron.py` | A cell with weights set by hand (1943) | "Take an umbrella?" from three yes/no facts. AND, OR and NOT from one cell each. Left or right mark with 400 hand-set weights: 1,000 of 1,000 cards right. Nothing learns yet. |
| `step2_learn.py` | The rule of 1958 | All 400 weights start at zero and change only after a wrong guess. On 2,000 fresh cards: 1,036 right before training, 1,724 after 20 cards, 2,000 after 200. In 10,000 cards it makes 14 mistakes, the last on card 145. |
| `step3_mark1.py` | The Mark I of 1960, rebuilt in numbers | 400 photocells, 512 middle units wired at random, 4 response units that learn. Names the letter wherever it sits: 250 of 1,000 before training, 976 of 1,000 after 10 passes. |
| `step4_converge.py` | The guarantee | If one straight line can split the two groups, the rule finds one, and the mistakes have a ceiling. 1,000 made-up problems: it stopped on every one and never came closer than 30% of the ceiling. |
| `step5_xor.py` | The wall of 1969 | The stairway lamp (on when exactly one switch is up): 1,000,000 cards, 480,332 weight changes, never more than 3 of 4 cases right. Of 9,261 cells tried, 0 do the lamp. Odd or even on 9 squares needs a middle unit that sees all 9. |
| `step6_hidden.py` | Two layers, the random way | Three cells set by hand do the lamp. With random middle cells and only the last cell learning, the cells needed grow fast: 32 for 2 switches, 64 for 4, 128 for 6, 256 for 8. |
| `step7_backprop.py` | The rule of 1986 | Cells answer on a smooth slope, so the mistake can be passed backward and every weight learns. The lamp with 2 middle cells: 62 of 100 random starts solve it; with 4 middle cells, 100 of 100. Letters with 4 trained middle cells: 1,000 of 1,000, against 976 for 512 random ones. |

`save.py` writes each step's numbers to `runs/`, and the animation reads them from there, so every number on screen comes from these runs.
Python 3.9 and 3.12 print the same output for all seven steps.

## What this is not

- Not the machine of 1960. `step3_mark1.py` keeps the Mark I's counts (400 photocells, 512 middle units) but the wiring, the thresholds and the letters are our choice. The scores are ours, not Rosenblatt's.
- The letters are small, clean drawings with a little noise. A photograph is a far harder problem.
- Passing the mistake backward does not always work on a small network: with 2 middle cells the lamp is solved from 62 of 100 starts, and odd or even with 6 switches from 5 of 10 starts.
- The 1986 paper (Rumelhart, Hinton, Williams) made the backward rule famous. Seppo Linnainmaa published the method in 1970 and Paul Werbos applied it to networks in 1982.

## Try it

Give the stairway lamp a third switch (the lamp is on when an odd number of switches are up) and find how many middle cells `step7_backprop.py` needs to solve it from every start.

MIT licence.
