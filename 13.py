from intcomputer import IntComputer
import intcomputer as ic
from copy import deepcopy


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4

SCREEN = {EMPTY: ' ',
          WALL: '▓',
          BLOCK: '◆',
          PADDLE: '▂',
          BALL: '◉'}


def get_n_outputs(comp, inputs, n):
    res = []
    for _ in range(n):
        if not comp.halted:
            res.extend(computer.reset_outputs().exec(inputs).get_outputs())
    return res


class Arcade:
    def __init__(self, data):
        self.score = 0
        self.scr = {}
        self.ball = (-1, -1)
        self.paddle = (-1, -1)
        self.blocks = 0
        self.max_x = self.max_y = 0
        for n in range(0, len(data), 3):
            self.scr[(data[n], data[n + 1])] = data[n + 2]
            if data[n + 2] == BLOCK:
                self.blocks += 1
            if data[n + 2] == BALL:
                self.ball = data[n], data[n + 1]
            if data[n + 2] == PADDLE:
                self.paddle = data[n], data[n + 1]
            self.max_x = max(data[n], self.max_x)
            self.max_y = max(data[n+1], self.max_y)

    def update(self, data):
        if not data:
            return
        if data[0] == -1:
            self.score = data[2]
        else:
            if self.scr[(data[0], data[1])] == BLOCK and data[2] != BLOCK:
                self.blocks -= 1
            if data[2] == PADDLE:
                self.paddle = (data[0], data[1])
            if data[2] == BALL:
                self.ball = (data[0], data[1])
            self.scr[(data[0], data[1])] = data[2]

    def __str__(self):
        sstr = '**** SCORE: {} * BLOCKS: {} * PADDLE: {} * BALL: {} ****\n'\
            .format(self.score, self.blocks, self.paddle, self.ball)
        for y in range(self.max_y):
            for x in range(self.max_x + 1):
                sstr = sstr + SCREEN[self.scr.get((x, y), EMPTY)]
            sstr += '\n'
        return sstr


with open("data/13.txt") as f:
    memory = [int(x) for x in f.readline().split(',')]

orig_memory = deepcopy(memory)
computer = IntComputer(memory, run_mode=ic.RUN_TO_HALT).exec()

print("Puzzle 13.1: ", sum([1 for item in computer.get_outputs()[2::3] if item == BLOCK]))


memory = deepcopy(orig_memory)
memory[0] = 2
computer = IntComputer(memory, run_mode=ic.PAUSE_ON_OUTPUT)

out = []
while True:
    o = get_n_outputs(computer, [], 3)
    out.extend(o)
    if o[0] == -1:
        break

arcade = Arcade(out)

JOY_LEFT = -1
JOY_RIGHT = 1
JOY_NEUTRAL = 0

DIR = JOY_NEUTRAL
while not computer.halted:
    arcade.update(get_n_outputs(computer, [DIR], 3))
    if arcade.paddle[0] < arcade.ball[0]:
        DIR = JOY_RIGHT
    elif arcade.paddle[0] > arcade.ball[0]:
        DIR = JOY_LEFT
    else:
        DIR = JOY_NEUTRAL

print("Puzzle 13.2: ", arcade.score)
