def fuelception(amount):
    amt = max(amount // 3 - 2, 0)
    if amt > 0:
        amt += fuelception(amt)
    return amt


with open("data/1.txt") as f:
    modules = [int(line) for line in f.readlines()]

fuel = 0
total_fuel = 0
for module in modules:
    module_fuel = module // 3 - 2
    fuel += module_fuel
    total_fuel += module_fuel + fuelception(module_fuel)

print("Puzzle 1.1: ", fuel)
print("Puzzle 1.2: ", total_fuel)
