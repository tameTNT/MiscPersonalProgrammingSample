from aocscrapper import get_AoC_input
import networkx as nx
import matplotlib.pyplot as plt

# get_AoC_input(2019, 14).strip().split("\n")
days_input = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""".strip().split("\n")

days_input = [recipe.split(" ") for recipe in days_input]
ingredients = set()
recipes = dict()
# recipe_relationships = nx.DiGraph()
final_result = False
for line in days_input:
    final_result = False
    constituents = list()
    for i in range(int((len(line)-1)/2)):
        if line[i*2] == '=&gt;' or line[i*2] == '=>':
            quantity = int(line[i*2+1])
            chemical = line[i*2+2].strip(",")
            final_result = (chemical, quantity)
        else:
            quantity = int(line[i*2])
            chemical = line[i*2+1].strip(",")
            constituents.append((chemical, quantity))

        ingredients.add(chemical)

    recipes[final_result] = constituents
    '''recipe_relationships.add_node(final_result[0])
    for (chemical, quantity) in constituents:
        recipe_relationships.add_edge(chemical, final_result[0])

nx.draw(recipe_relationships, with_labels=True)
plt.show()'''

fuel_created = 0

quantities_needed = [("FUEL", 1)]
while not fuel_created:
    for ingredient in quantities_needed:
        amount = ingredient[1]
        
