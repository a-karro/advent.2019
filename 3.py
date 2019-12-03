DIRS = {'R': (1, 0),
        'D': (0, -1),
        'L': (-1, 0),
        'U': (0, 1)}


def build_line(line_data):
    x = 0
    y = 0
    line = {}
    step_counter = 0
    for item in line_data:
        for i in range(int(item[1:])):
            x += DIRS[item[0]][0]
            y += DIRS[item[0]][1]
            step_counter += 1
            line[(x, y)] = step_counter
    return line


with open("data/3.txt") as f:
    line1 = build_line([item.strip() for item in f.readline().split(',')])
    line2 = build_line([item.strip() for item in f.readline().split(',')])

dists = []
signals = []
for point in line1.keys():
    if point in line2.keys():
        dists.append(abs(point[0]) + abs(point[1]))
        signals.append(line1[point] + line2[point])


dists.sort()
print("Puzzle 3.1: ", dists[0])

signals.sort()
print("Puzzle 3.2: ", signals[0])
