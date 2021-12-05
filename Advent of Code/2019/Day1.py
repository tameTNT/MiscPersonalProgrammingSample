from aocscrapper import get_AoC_input

days_input = get_AoC_input(2019, 1).strip().split("\n")
total_fuel_required = 0


def calculate_fuel(mass):
    mass /= 3
    mass = int(mass)  # only take integer part - i.e. round down
    mass -= 2
    fuel_required = mass
    return fuel_required


for module in days_input:
    module = int(module)
    total_fuel_required += calculate_fuel(module)

print(f"Part 1: {total_fuel_required}")

total_fuel_required = 0
for module in days_input:
    module = int(module)
    while True:
        fuel = calculate_fuel(module)
        if fuel <= 0:
            break
        total_fuel_required += fuel
        module = fuel

print(f"Part 2: {total_fuel_required}")
