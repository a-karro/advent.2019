def is_good(number):
    s = str(number)
    double = False
    for i in range(len(s)-1):
        if s[i] > s[i+1]:
            return False
        double = double or s[i] == s[i+1]
    return double


def is_better(number):
    number = str(number)
    for i in range(10):
        s = str(i) * 2
        s1 = str(i) * 3
        if number.count(s) > 0 and number.count(s1) == 0:
            return True
    return False


with open("data/4.txt") as f:
    start, finish = (int(item) for item in f.readline().split('-'))

goods = [item for item in range(start, finish+1) if is_good(item)]
betters = [item for item in goods if is_better(item)]

print("Puzzle 4.1: ", len(goods))
print("Puzzle 4.2: ", len(betters))
