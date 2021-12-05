from aocscrapper import get_AoC_input
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_s = [int(x) for x in get_AoC_input(2020, 10).strip().split('\n')]
    input_s.append(0)
    input_s.append(max(input_s) + 3)
    input_s.sort()

    diff_list = list()
    for i in range(1, len(input_s)):
        diff_list.append(input_s[i] - input_s[i-1])

    print('Part 1:', diff_list.count(1) * (diff_list.count(3)))

    set_s = set(input_s)

    p_graph = nx.DiGraph()
    for i in input_s:
        x = 1
        while True:
            if x > 3:
                break

            if i + x in input_s:
                p_graph.add_edge(i, i + x)
                x += 1
            elif x < 3:
                x += 1
            else:
                break

    draw_graph = False
    if draw_graph:
        pos = nx.spring_layout(p_graph)
        nx.draw_networkx(p_graph, pos=pos, with_labels=False, node_size=50)
        nx.draw_networkx_labels(p_graph, pos=pos)
        plt.show()

    # theoretical help from https://discord.com/channels/267624335836053506/782715290437943306/786661174179528714
    nx.set_node_attributes(p_graph, 1, 'num_pre_nodes')

    for x in input_s[1:]:
        pre_nodes = [s for (s, d) in p_graph.in_edges(nbunch=x)]
        p_graph.nodes[x]['num_pre_nodes'] = sum([p_graph.nodes[node]['num_pre_nodes'] for node in pre_nodes])

    print('Part 2:', p_graph.nodes[max(input_s)]['num_pre_nodes'])  # len(list(nx.all_simple_paths(p_graph, 0, max(input_s)))) too slow
