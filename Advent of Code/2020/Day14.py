from aocscrapper import get_AoC_input
import re

if __name__ == '__main__':
    input_s = [x for x in get_AoC_input(2020, 14, get_test=False).strip().split('\n')]

    def apply_mask(val, m, registers, m_address, part2=False):
        results = ['']  # a list of possible binary strings - in part 1, this list is always just length 1
        bin_val = bin(val)[2:].zfill(36)
        bin_m_address = bin(m_address)[2:].zfill(36)
        for i in range(36):  # going bit by bit through mask
            if m[i] == '1':
                if not part2:
                    results[0] += '1'
                else:
                    results = [x + '1' for x in results]
            elif m[i] == '0':
                if not part2:
                    results[0] += '0'
                else:
                    results = [x + bin_m_address[i] for x in results]
            elif m[i] == 'X':
                if not part2:
                    results[0] += bin_val[i]
                else:
                    poss0_set = [x + '0' for x in results]
                    poss1_set = [x + '1' for x in results]
                    results = poss0_set + poss1_set

        # writing data to memory addresses
        if not part2:
            # int('???', 2)converts from binary to decimal
            registers[m_address] = int(results[0], 2)
        else:
            for a in results:  # for each possible memory address generated
                registers[int(a, 2)] = val

    def step_through(part2=False):
        memory_registers = dict()
        mask = bin(0)[2:].zfill(36)
        for instruction in input_s:
            ins_type, value = instruction.split(' = ')
            if ins_type[:3] == 'mas':  # mask instruction
                mask = value
            else:  # memory register instruction
                address = int(re.findall(r'\d+', ins_type)[0])  # captures address from within instruction e.g. mem[90]
                if not part2:
                    apply_mask(int(value), mask, memory_registers, address)
                else:
                    apply_mask(int(value), mask, memory_registers, address, part2)

        return sum(memory_registers.values())

    print('Part 1:', step_through())  # 15172047086292
    print('Part 2:', step_through(part2=True))  # 4197941339968
