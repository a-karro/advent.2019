import copy
from intcomputer import IntComputer

with open("data/5.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

orig_memory = copy.deepcopy(memory)

print("Puzzle 5.1: ", IntComputer(memory).exec([1]).get_last_output())
memory = copy.deepcopy(orig_memory)
print("Puzzle 5.2: ", IntComputer(memory).exec([5]).get_last_output())
