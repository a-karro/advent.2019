import copy
import intcomputer as ic

with open("data/2.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

orig_memory = copy.deepcopy(memory)

memory[1] = 12
memory[2] = 2

ic.intcomputer(memory, 0, [])
print("Puzzle 2.1: ", memory[0])

noun = 0
for n in range(100):
    memory = copy.deepcopy(orig_memory)
    memory[1] = n
    memory[2] = 0
    ic.intcomputer(memory, 0, [])
    if memory[0] > 19690720:
        noun = n - 1
        break

verb = 0
for v in range(100):
    memory = copy.deepcopy(orig_memory)
    memory[1] = noun
    memory[2] = v
    ic.intcomputer(memory, 0, [])
    if memory[0] == 19690720:
        verb = v
        break

print("Puzzle 2.2: ", noun * 100 + verb)
