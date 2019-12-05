import copy

with open("data/5.txt") as f:
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


def intcomputer(mem, input_value):
    pointer = 0
    last_output = None
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
            mem[mem[pointer + 1]] = input_value
            pointer += 2
        elif opcode == OUT:
            last_output = op1
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
    return last_output


orig_memory = copy.deepcopy(memory)


print("Puzzle 5.1: ", intcomputer(memory, 1))

memory = copy.deepcopy(orig_memory)
print("Puzzle 5.2: ", intcomputer(memory, 5))
