import copy
from itertools import permutations
from intcomputer import IntComputer
import intcomputer as ic

with open("data/7.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

orig_memory = copy.deepcopy(memory)
max_thrust = -99999999999
perm = permutations([0, 1, 2, 3, 4])

for phases in perm:
    next_inp = 0
    for phase in phases:
        memory = copy.deepcopy(memory)
        next_inp = IntComputer(memory).exec([phase, next_inp]).get_last_output()
    max_thrust = max(max_thrust, next_inp)

print("Puzzle 7.1: ", max_thrust)

max_thrust = -99999999999
perm = permutations([5, 6, 7, 8, 9])

for p in perm:
    computers = []
    for i in range(5):
        computers.append(IntComputer(copy.deepcopy(memory), run_mode=ic.PAUSE_ON_OUTPUT))

    i2 = 0
    while [c.halted for c in computers] != [True] * 5:
        for i in range(5):
            i1 = p[i] if computers[i].cold else i2
            i2 = computers[i].exec([i1, i2]).get_last_output()
        max_thrust = max(max_thrust, computers[4].get_last_output())

print("Puzzle 7.2: ", max_thrust)
