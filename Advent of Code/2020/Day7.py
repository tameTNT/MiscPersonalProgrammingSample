from aocscrapper import get_AoC_input
import networkx as nx

if __name__ == '__main__':
    input_s = get_AoC_input(2020, 7).strip()
    input_s = input_s.split('\n')

    bag_rules = nx.DiGraph()
    for rule in input_s:
        start_bag = rule.split(' bags contain')[0]
        contains = rule.split(' bags contain')[1].split(', ')
        for bag in contains:
            if bag != ' no other bags.':
                n, colour = bag.strip().split(' ', maxsplit=1)
                n = int(n)
                colour = colour.rsplit(' ', maxsplit=1)[0]
                bag_rules.add_edge(start_bag, colour, n=n)

    print('Part 1:', len(nx.ancestors(bag_rules, 'shiny gold')))

    def explore_cost(root_node):
        cost = 0
        for edge in bag_rules.out_edges(root_node):
            num_bags_inside = bag_rules.edges[edge]['n']
            cost += num_bags_inside + explore_cost(edge[1]) * num_bags_inside
        return cost

    print('Part 2:', explore_cost('shiny gold'))
