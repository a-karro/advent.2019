from intcomputer import IntComputer

with open("data/9.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

print("Puzzle 9.1: ", IntComputer(memory).exec([1]).get_last_output())
print("Puzzle 9.2: ", IntComputer(memory).exec([2]).get_last_output())
