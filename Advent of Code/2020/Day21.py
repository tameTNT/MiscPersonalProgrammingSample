from aocscrapper import get_AoC_input
import re
from collections import Counter

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 21, get_test=True).strip().split('\n')]

    foods = [(f.strip(')').split(' (contains ')) for f in input_s]

    ingredients_listed = list()
    for f in foods:
        ingredients_listed += f[0].split(' ')
    ingredient_count = Counter(ingredients_listed)

    foods = [{'in': set(i.split(' ')), 'all': set(a.split(', '))} for (i, a) in foods]

    all_ingredients = set.union(*[f['in'] for f in foods])

    possible_matches = {i: set() for i in all_ingredients}

    print('Part 1:', sum(ingredient_count.values()))
