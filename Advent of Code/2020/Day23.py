from aocscrapper import get_AoC_input

if __name__ == '__main__':
    original_cup_list = [int(x) for x in list(get_AoC_input(2020, 23, get_test=True).strip())]
    cup_list = list(original_cup_list)

    def circ_index(i, l):
        return i % len(l)

    current_cup = cup_list[0]
    for x in range(100):
        held_list = list()
        for i in range(3):
            current_index = cup_list.index(current_cup)
            held_list.append(cup_list.pop(circ_index(current_index+1, cup_list)))

        current_index = cup_list.index(current_cup)
        destination_cup = cup_list[circ_index(current_index, cup_list)] - 1
        while destination_cup not in cup_list:
            if destination_cup < min(cup_list):
                destination_cup = max(cup_list)
            else:
                destination_cup -= 1
        destination_index = circ_index(cup_list.index(destination_cup) + 1, cup_list)
        for i in range(3):
            cup_list.insert(destination_index + i, held_list.pop(0))

        current_cup = cup_list[circ_index(cup_list.index(current_cup) + 1, cup_list)]

    start_index = circ_index(cup_list.index(1) + 1, cup_list)
    answer_str = ''
    for i in range(len(cup_list)-1):
        answer_str += str(cup_list[circ_index(start_index+i, cup_list)])

    print('Part 1:', answer_str)

    cup_list = list(original_cup_list + [x for x in range(max(original_cup_list), 1000001)])

    class Cup:
        def __init__(self, label):
            self.label = label
            self.next = None

        def __eq__(self, other):
            return self.label == other

    for x in range(10000000):
        # TODO: setup linked list
        pass
