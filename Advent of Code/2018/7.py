import networkx as nx

with open("Inputs\\Day7.txt", "r") as file_obj:
    graph = nx.DiGraph()
    instructions = [line.strip() for line in file_obj]
    for instruction in instructions:
        graph.add_edge(instruction.split(" ")[1], instruction.split(" ")[-3])

    print("Part 1: ", "".join(nx.lexicographical_topological_sort(graph)))
