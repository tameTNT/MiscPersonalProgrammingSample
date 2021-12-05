from aocscrapper import get_AoC_input
from collections import Counter

if __name__ == '__main__':
    input_s = get_AoC_input(2020, 6).strip().split('\n\n')

    people_groups = [group.split('\n') for group in input_s]

    count = 0
    for group in people_groups:
        yes_questions = Counter(''.join(group))
        count += len(yes_questions.keys())  # len(set.union(*[set(p) for p in group])) - this finds all unique answers

    print('Part 1:', count)

    count = 0
    for group in people_groups:
        total_count = Counter()
        target_count = len(group)
        for person in group:
            p = Counter(person)
            total_count.update(p)

        count += list(total_count.values()).count(target_count)  # len(set.intersection(*[set(p) for p in group])) - this finds answers common across all people

    print('Part 2:', count)
