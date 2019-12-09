import intcomputer as ic

with open("data/9.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

print("Puzzle 9.1: ", ic.intcomputer(memory, 0, [1], print_output=False)[0])
print("Puzzle 9.2: ", ic.intcomputer(memory, 0, [2], print_output=False)[0])
