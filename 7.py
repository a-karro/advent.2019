import copy
from itertools import permutations

with open("data/7.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

POS = 0
IMM = 1

ADD = 1
MUL = 2
INP = 3
OUT = 4
JIT = 5
JIF = 6
LES = 7
EQU = 8
HLT = 99

PAUSE_ON_OUTPUT = 1
RUN_TO_HALT = 2


def intcomputer(mem, input_values, op_mode=RUN_TO_HALT):
    pointer = 0
    last_output = None
    input_counter = 0
    while mem[pointer] != 99:
        act = mem[pointer]
        opcode = act % 100
        if opcode not in [ADD, MUL, INP, OUT, JIT, JIF, LES, EQU, HLT]:
            raise ValueError("wrong opcode {} at position {}".format(act, pointer))
        m1 = act // 100 % 10
        m2 = act // 1000 % 10
        op1 = mem[mem[pointer + 1]] if m1 == POS else mem[pointer + 1]
        if opcode not in [INP, OUT]:
            op2 = mem[mem[pointer + 2]] if m2 == POS else mem[pointer + 2]
        else:
            op2 = None

        if opcode == INP:
            if input_counter > len(input_values):
                raise ValueError("No more input values")
            mem[mem[pointer + 1]] = input_values[input_counter]
            input_counter += 1
            pointer += 2
        elif opcode == OUT:
            last_output = op1
            if op_mode == PAUSE_ON_OUTPUT:
                input_values = yield
                yield last_output
            pointer += 2
        elif opcode == ADD:
            mem[mem[pointer + 3]] = op1 + op2
            pointer += 4
        elif opcode == MUL:
            mem[mem[pointer + 3]] = op1 * op2
            pointer += 4
        elif opcode == JIT:
            if op1 != 0:
                pointer = op2
            else:
                pointer += 3
        elif opcode == JIF:
            if op1 == 0:
                pointer = op2
            else:
                pointer += 3
        elif opcode == LES:
            mem[mem[pointer + 3]] = 1 if op1 < op2 else 0
            pointer += 4
        else:
            mem[mem[pointer + 3]] = 1 if op1 == op2 else 0
            pointer += 4

        if pointer > len(mem) - 1:
            raise ValueError("Pointer out of range")
    if op_mode == RUN_TO_HALT:
        yield last_output


orig_memory = copy.deepcopy(memory)

max_thrust = -99999999999

perm = permutations([0, 1, 2, 3, 4])
for p in perm:
    out = 0
    for k in p:
        memory = copy.deepcopy(memory)
        out_gen = intcomputer(memory, [k, out])
        out = next(out_gen)
    max_thrust = max(max_thrust, out)

print("Puzzle 7.1: ", max_thrust)


perm = permutations([5, 6, 7, 8, 9])
max_thrust = -99999999999

for p in perm:
    computers = []
    for k in p:
        computers.append(intcomputer(copy.deepcopy(orig_memory), [k, 0], PAUSE_ON_OUTPUT))

    for i, k in enumerate(p):
        out = next(computers[i])
        computers[(i + 1) % 5].send([p[(i + 1) % 5], out])

    max_thrust = max(max_thrust, out)
