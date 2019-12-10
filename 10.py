import math


def dist(a, b):
    return round(math.sqrt((a[0]-b[0])**2 + (a[1] - b[1])**2), 30)


def angle_from_zero(p1, p2):
    x_diff = p2[0] - p1[0]
    y_diff = p2[1] - p1[1]
    return round(math.degrees(math.atan2(y_diff, x_diff)), 30)


points = []
with open('data/10.txt') as f:
    for y, line in enumerate(f.readlines()):
        points.extend([{'point': (x, y), 'angle': 0, 'dtl': 0} for x, point in enumerate(line) if point == '#'])


max_visible = 0
position = 0

distances = {}

for i, beg in enumerate(points):
    for j, end in enumerate(points[:i] + points[i+1:]):
        distances[beg['point'], end['point']] = dist(beg['point'], end['point'])


for i, beg in enumerate(points):
    other_points = points[:i] + points[i+1:]
    seen = 0
    for j, end in enumerate(other_points):
        rem_points = other_points[:j] + other_points[j+1:]
        sees_the_end = True
        for middle in rem_points:
            beg_to_mid = distances[beg['point'], middle['point']]
            mid_to_end = distances[middle['point'], end['point']]
            beg_to_end = distances[beg['point'], end['point']]
            sees_the_end = sees_the_end and round(beg_to_mid + mid_to_end, 10) != round(beg_to_end, 10)
            if not sees_the_end:
                break
        seen += 1 if sees_the_end else 0
    if seen > max_visible:
        max_visible = seen
        position = i
print("Puzzle 10.1: ", max_visible)

laser = points[position]['point']

targets = points

for point in targets:
    angle1 = 270
    angle2 = angle_from_zero(laser, point['point'])
    point['angle'] = round((angle2 - angle1) % 360, 10)
    point['dtl'] = dist(laser, point['point'])

targets = sorted(targets, key=lambda d: (d['angle'], 20, d['dtl']))

cnt = 0
while len(targets) > 0 and cnt < 200:
    cur_angle = None
    shot = []
    for target in targets:
        if cur_angle == target['angle']:
            continue
        else:
            cur_angle = target['angle']
            shot.append(target)
            cnt += 1
            if cnt == 200:
                print('Puzzle 10.2: ', target['point'][0] * 100 + target['point'][1])
                exit(0)
    for dust in shot:
        targets.remove(dust)
