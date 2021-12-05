import networkx as nx
from aocscrapper import get_AoC_input
import matplotlib.pyplot as plt

days_input = get_AoC_input(2019, 6).strip().split("\n")
days_input = [orbit.split(")") for orbit in days_input]

orbit_graph = nx.Graph()

# builds graphs from input data
for orbit_relationship in days_input:
    a = orbit_relationship[0]
    b = orbit_relationship[1]
    if a not in orbit_graph.nodes:
        orbit_graph.add_node(a)
    if b not in orbit_graph.nodes:
        orbit_graph.add_node(b)
    orbit_graph.add_edge(a, b)

total_orbits = 0
relationships = dict(nx.all_pairs_shortest_path_length(orbit_graph))
for planet in orbit_graph.nodes:
    total_orbits += relationships["COM"][planet]

print("Part 1:", total_orbits)

# -2 is to account for not counting starting and end orbits
total_transfers = nx.shortest_path_length(orbit_graph, "SAN", "YOU") - 2
print("Part 2:", total_transfers)

# optional visualisation of graph
draw_graph = False
if draw_graph:
    planet_positions = nx.spring_layout(orbit_graph, k=10/(orbit_graph.order())**0.5)
    nx.draw_networkx(orbit_graph, pos=planet_positions, with_labels=False, node_size=50)
    nx.draw_networkx_labels(orbit_graph, pos=planet_positions, labels={"COM": "CoM", "SAN": "Santa", "YOU": "You"})
    plt.show()
