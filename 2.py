import copy

with open("data/2.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]


def intcomputer(mem):
    pointer = 0
    while mem[pointer] != 99:
        if mem[pointer] not in [1, 2, 99]:
            raise ValueError("Oh Noes, unknown opcode {} at position {}".format(mem[pointer], pointer))
        act = mem[pointer]
        op1 = mem[mem[pointer + 1]]
        op2 = mem[mem[pointer + 2]]
        out = mem[pointer + 3]
        mem[out] = op1 + op2 if act == 1 else op1 * op2
        pointer += 4
        if pointer > len(mem) - 1:
            raise ValueError("Pointer out of range")
    return mem


orig_memory = copy.deepcopy(memory)

memory[1] = 12
memory[2] = 2

print("Puzzle 2.1: ", intcomputer(memory)[0])

noun = 0
for n in range(100):
    memory = copy.deepcopy(orig_memory)
    memory[1] = n
    memory[2] = 0
    if intcomputer(memory)[0] > 19690720:
        noun = n - 1
        break

verb = 0
for v in range(100):
    memory = copy.deepcopy(orig_memory)
    memory[1] = noun
    memory[2] = v
    if intcomputer(memory)[0] == 19690720:
        verb = v
        break

print("Puzzle 2.2: ", noun * 100 + verb)
