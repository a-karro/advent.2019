import copy
import intcomputer as ic

with open("data/5.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

orig_memory = copy.deepcopy(memory)


print("Puzzle 5.1: ", ic.intcomputer(memory, 0, [1])[0])

memory = copy.deepcopy(orig_memory)
print("Puzzle 5.2: ", ic.intcomputer(memory, 0, [5])[0])
