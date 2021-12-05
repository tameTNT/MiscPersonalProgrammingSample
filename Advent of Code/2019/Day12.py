from aocscrapper import get_AoC_input
from itertools import combinations
from operator import add, abs
import numpy as np

# pre-processing weird coord input
days_input = get_AoC_input(2019, 12).strip().split("\n")
days_input = [dim.split("=")[1:] for dim in days_input]
days_input = [[int(item.split(",")[0].strip(">")) for item in planet] for planet in days_input]
moon_list = ("Io", "Europa", "Ganymede", "Callisto")
moon_pairings = list(combinations(moon_list, 2))


def simulate_step(moon_names, pairs, positions, velocities):
    """Simulates one time step of gravity affecting velocities and these altering positions. Returns positions and velocities"""
    # Gravity and velocity calculation and manipulation
    for moon_pair in pairs:
        moon1 = moon_pair[0]
        moon2 = moon_pair[1]
        for dim in (0, 1, 2):  # x, y, z gravity calculations to adjust velocities
            moon1_pos = positions[moon1][dim]
            moon2_pos = positions[moon2][dim]

            if moon1_pos > moon2_pos:
                velocities[moon1][dim] -= 1
                velocities[moon2][dim] += 1
            elif moon1_pos < moon2_pos:
                velocities[moon1][dim] += 1
                velocities[moon2][dim] -= 1
            # NB: if equal, no effect
    # Updates positions based on velocities
    for moon in moon_names:
        positions[moon] = list(map(add, positions[moon], velocities[moon]))

    return positions, velocities


moon_positions = {moon_list[i]: list(days_input[i]) for i in range(len(moon_list))}
moon_velocities = {moon_list[i]: [0]*3 for i in range(len(moon_list))}
for i in range(1000):
    simulate_step(moon_list, moon_pairings, moon_positions, moon_velocities)

# Gets the absolute values of all the x,y and z coords/velocities for all the moons and adds them up
moon_potential_energies = {moon: sum(map(abs, moon_positions[moon])) for moon in moon_list}
moon_kinetic_energies = {moon: sum(map(abs, moon_velocities[moon])) for moon in moon_list}
total_energy = 0
for moon in moon_list:
    total_energy += moon_potential_energies[moon] * moon_kinetic_energies[moon]
print("Part 1:", total_energy)


# Theory of independent axes and then finding lcm - REDDIT RIPPED (No. 4)
past_states = [set(), set(), set()]  # use of sets for speed purposes
cycles = [False, False, False]  # all start as False - i.e. no cycles found yet

moon_positions = {moon_list[i]: list(days_input[i]) for i in range(len(moon_list))}
moon_velocities = {moon_list[i]: [0]*3 for i in range(len(moon_list))}
while not(cycles[0] and cycles[1] and cycles[2]):  # halts once cycle length for all 3 axes found
    simulate_step(moon_list, moon_pairings, moon_positions, moon_velocities)
    for dim in (0, 1, 2):  # x, y, z axes considered separately as they are all independent
        current_state = (tuple(list(planet_xyz)[dim] for planet_xyz in moon_positions.values()),
                         tuple(list(planet_xyz)[dim] for planet_xyz in moon_velocities.values()))
        if current_state in past_states[dim] and not cycles[dim]:
            cycles[dim] = len(past_states[dim])  # cycle length is steps since start of simulation
        else:
            past_states[dim].add(current_state)

print("Part 2:", np.lcm.reduce(cycles, dtype="int64"))  # dtype required as otherwise an overflow error occurs
