import re
import itertools
import copy

moons = []

with open('data/12.txt') as f:
    for line in f.readlines():
        moons.append([int(i) for i in re.findall(r'-?\d+', line)] + [0] * 3)


step_limit = 1000

pairs = list(itertools.combinations(list(range(len(moons))), 2))


def gravity_well():
    for p in range(len(pairs)):
        om1 = moons[pairs[p][0]]
        om2 = moons[pairs[p][1]]
        velodelta1 = [0, 0, 0]
        velodelta2 = [0, 0, 0]
        for n in range(3):
            if om1[n] < om2[n]:
                velodelta1[n] = 1
                velodelta2[n] = -1
            elif om1[n] > om2[n]:
                velodelta1[n] = -1
                velodelta2[n] = 1
            else:
                pass
        nm1 = om1
        nm2 = om2
        for n in range(3):
            nm1[n+3] = om1[n+3] + velodelta1[n]
            nm2[n+3] = om2[n+3] + velodelta2[n]
        moons[pairs[p][0]] = nm1
        moons[pairs[p][1]] = nm2

    for n in range(len(moons)):
        for c in range(3):
            moons[n][c] = moons[n][c] + moons[n][c+3]


for i in range(step_limit):
    gravity_well()
tot = 0
for t in range(len(moons)):
    pot = kin = 0
    for c in range(3):
        pot += abs(moons[t][c])
        kin += abs(moons[t][c+3])
    tot = tot + pot * kin

print("Puzzle 12.1: ", tot)
