from intcomputer import IntComputer
import intcomputer as ic
from copy import deepcopy

with open("data/11.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]


DELTAS = {'L': (-1, 0),
          'D': (0, 1),
          'R': (1, 0),
          'U': (0, -1)}

DIRS = {'U': ('L', 'R'),
        'L': ('D', 'U'),
        'D': ('R', 'L'),
        'R': ('U', 'D')}


def painter(h, mem):
    _x = _y = 0
    direction = 'U'
    computer = IntComputer(mem, run_mode=ic.PAUSE_ON_OUTPUT)
    while not computer.halted:
        inp = h.get((_x, _y), 0)
        paint_to = computer.exec([inp]).get_last_output()
        if not computer.halted:
            turn_to = computer.exec([inp]).get_last_output()
        else:
            break
        h[(_x, _y)] = paint_to
        direction = DIRS[direction][turn_to]
        dx, dy = DELTAS[direction]
        _x += dx
        _y += dy


orig_mem = deepcopy(memory)

hull = {}
painter(hull, memory)

print("Puzzle 1: ", len(hull))

memory = deepcopy(orig_mem)
hull = {(0, 0): 1}
painter(hull, memory)

minX = min(coord[0] for coord in hull.keys())
maxX = max(coord[0] for coord in hull.keys())

minY = min(coord[1] for coord in hull.keys())
maxY = max(coord[1] for coord in hull.keys())

print("Puzzle 11.2: ")
for y in range(minY, maxY + 1):
    sstr = ''
    for x in range(minX, maxX + 1):
        sstr += '##' if hull.get((x, y), 0) == 1 else '  '
    print(sstr)
