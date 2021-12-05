from aocscrapper import get_AoC_input
import re

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 16, get_test=False).strip().split('\n\n')]
    
    rules, own_ticket, nearby_tickets = input_s
    own_ticket = own_ticket.split('\n', maxsplit=1)[1].split(',')
    nearby_tickets = nearby_tickets.split('\n', maxsplit=1)[1]

    rule_dict = dict()
    for line in rules.split('\n'):
        ranges = re.findall(r'(\d+)-(\d+)', line)
        rule_dict[line.split(':')[0]] = [range(int(x), int(y)+1) for (x, y) in ranges]

    full_poss_valid = set()
    for range_set in rule_dict.values():
        for r in range_set:
            full_poss_valid = full_poss_valid.union(set(r))

    scanning_error_rate = 0
    valid_tickets = list()
    for t in nearby_tickets.split('\n'):
        nums = [int(n) for n in t.split(',')]
        valid = True
        for n in nums:
            if n not in full_poss_valid:
                scanning_error_rate += n
                valid = False
        if valid:
            valid_tickets.append(nums)

    print('Part 1:', scanning_error_rate)

    num_fields = len(rule_dict)
    valid_field_vals = [{t[i] for t in valid_tickets} for i in range(num_fields)]  # list of sets of values for each field index

    field_index_map = {name: set() for name in rule_dict.keys()}  # maps each field name to a set of index possibilities
    for i, field in enumerate(valid_field_vals):
        for name, vranges in rule_dict.items():
            if field < set.union(*[set(r) for r in vranges]):  # i.e. field is a subset of ranges
                field_index_map[name].add(i)  # this field name could correspond to this row

    # remove duplicate possibilities for each field by elimination and figure out only possible mapping of fields and indexes
    def count_multi_sets(d):
        """Counts number of values in dictionary where set is larger than 1 item"""
        count = 0
        for s in d.values():
            if isinstance(s, set):  # if it's an int then it's already been decided
                count += 1
        return count

    decided = set()
    while count_multi_sets(field_index_map) != 0:  # keep looping until every field's been successfully mapped
        for name, poss in field_index_map.items():
            if isinstance(poss, set):  # otherwise it's an int and it's already been decided
                to_remove = list()  # to avoid changing set size during iteration below
                for n in poss:
                    if n in decided:
                        to_remove.append(n)
                for r in to_remove:
                    poss.remove(r)

                if len(poss) == 1:  # i.e. only one index possibility left in set for this field - this must be the correct index then
                    index = poss.pop()
                    decided.add(index)
                    field_index_map[name] = index

    multiply_value = 1
    for field_name, index in field_index_map.items():
        if 'departure' in field_name:
            multiply_value *= int(own_ticket[index])

    print('Part 2:', multiply_value)
