def spacewalk(start, count, orbs):
    if start not in orbs.keys():
        return count, 0 if start == "YOU" else None, 0 if start == "SAN" else None
    cnt = 0
    you = santa = None
    for orb in orbs[start]:
        stats = spacewalk(orb, count + 1, orbs)
        cnt += stats[0]
        you = stats[1] + 1 if stats[1] is not None else you
        santa = stats[2] + 1 if stats[2] is not None else santa
        if you and santa:
            santa_and_you.append(you + santa)
    return cnt + count, you, santa


with open('data/6.txt') as f:
    orbits = {}
    for line in f.readlines():
        key, value = line.split(')')
        current = orbits.get(key, [])
        current.append(value.strip())
        orbits[key] = current

com = [key for key in orbits.keys() if key not in [x for y in orbits.values() for x in y]][0]
santa_and_you = []

print("Puzzle 6.1: ", spacewalk(com, 0, orbits)[0])
santa_and_you.sort()
print("Puzzle 6.2: ", santa_and_you[0] - 2)
