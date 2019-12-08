with open('data/8.txt') as f:
    pixels = [int(ch) for ch in f.readline()]

w = 25
h = 6

least_zeros = -1
min_zeros = len(pixels) + 1

layers = []
for i in range(0, len(pixels), w * h):
    layers.append(pixels[i:i + w * h])

for i, layer in enumerate(layers):
    zeros = layer.count(0)
    if zeros < min_zeros:
        min_zeros = zeros
        least_zeros = i

print("Puzzle 8.1: ", layers[least_zeros].count(1) * layers[least_zeros].count(2))

print("Puzzle 8.2:")
for y in range(h):
    sstr = ' '
    for x in range(w):
        for d in range(len(layers)):
            px = layers[d][y * w + x]
            if px == 2:
                continue
            else:
                sstr += '##' if px == 1 else '  '
                break
    print(sstr)
