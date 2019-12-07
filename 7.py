import copy
from itertools import permutations
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
        next_inp = ic.intcomputer(memory, 0, [phase, next_inp], op_mode=ic.RUN_TO_HALT)[0]
    max_thrust = max(max_thrust, next_inp)

print("Puzzle 7.1: ", max_thrust)

max_thrust = -99999999999
perm = permutations([5, 6, 7, 8, 9])

for p in perm:
    memories = []
    for k in p:
        memories.append({'memory': copy.deepcopy(orig_memory), 'pointer': 0,
                         'phase': k, 'last': None, 'ran': False})
    next_inp = 0
    while [m['pointer'] for m in memories] != [-1] * 5:
        for i in range(5):
            o, point = ic.intcomputer(memories[i]['memory'], memories[i]['pointer'],
                                      [memories[i]['phase'] if not memories[i]['ran'] else next_inp, next_inp],
                                      op_mode=ic.PAUSE_ON_OUTPUT)
            memories[i]['ran'] = True
            memories[i]['pointer'] = point
            next_inp = o or next_inp
            memories[i]['last'] = o or memories[i]['last']

        max_thrust = max(max_thrust, memories[4]['last'])

print("Puzzle 7.2: ", max_thrust)
