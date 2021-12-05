from aocscrapper import get_AoC_input
import re
import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 20, get_test=False).strip().split('\n\n')]
    tile_dict = {int(re.findall(r'Tile (\d+):', t.split('\n', maxsplit=1)[0])[0]):
                 t.split('\n', maxsplit=1)[1] for t in input_s}

    edges_dict = dict()  # mapping of each possible edge to 'owning' keys


    def add_edge(d, el, i):
        """Adds string edges in list, el, as keys to dictionary, d, adding id, i, to each key's set"""
        for e in el:
            if e not in d.keys():
                d[e] = set()
            d[e].add(i)


    for t_id, tile in tile_dict.items():
        tile_as_list = [list(x) for x in tile.split('\n')]
        top_edge = ''.join(tile_as_list[0])
        right_edge = ''.join([row[-1] for row in tile_as_list])
        bottom_edge = ''.join(tile_as_list[-1])
        left_edge = ''.join([row[0] for row in tile_as_list])

        edges_to_add = [top_edge, top_edge[::-1],
                        right_edge, right_edge[::-1],
                        bottom_edge, bottom_edge[::-1],
                        left_edge, left_edge[::-1]]  # includes flipped/reversed versions of each edge

        add_edge(edges_dict, edges_to_add, t_id)

    match_up_count = {t_id: 0 for t_id in tile_dict.keys()}
    image_graph = nx.Graph()
    for edge in edges_dict:
        if len(edges_dict[edge]) != 1:  # i.e. edge has no matches with any others
            for tile in edges_dict[edge]:
                match_up_count[tile] += 1
            image_graph.add_edges_from([tuple(edges_dict[edge])])

    match_up_count = {t_id: c//2 for t_id, c in match_up_count.items()}  # halves all values in the dictionary since each edge pair will be counted twice

    id_multiply = 1
    for tile_id, count in match_up_count.items():
        if count == 2:  # i.e. an edge tile with only 2 pairs
            id_multiply *= tile_id

    print('Part 1:', id_multiply)

    # to draw graph
    if True:
        nx.draw_networkx(image_graph, with_labels=True, node_size=10)
        plt.show()

    # image_edge_len = int(len(tile_dict)**0.5)
    # grid_graph = nx.grid_2d_graph(image_edge_len, image_edge_len)
