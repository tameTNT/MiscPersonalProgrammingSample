import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

with open("Inputs\\Day 7 Input.txt") as input_set:
    for line in input_set:
        name = line.split()[0]

        G.add_node(name, weight=int(line.split()[1].strip("()")))

        if "->" in line:
            child_list = [child.strip() for child in line.split("->")[1].split(",")]

            for child in child_list:
                G.add_edge(name, child)

    list_ = list(nx.topological_sort(G))

    print(list_[0])

    plt.subplot(111)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
