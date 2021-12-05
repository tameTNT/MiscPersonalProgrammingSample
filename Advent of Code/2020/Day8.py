from aocscrapper import get_AoC_input

if __name__ == '__main__':
    input_s = get_AoC_input(2020, 8).strip().split('\n')

    def run_code(code_list, part2=False):
        i = 0
        accumulator = 0
        visited = set()
        while i not in visited:
            visited.add(i)
            try:
                inst, arg = code_list[i].split(' ')
            except IndexError:  # trying to access line beyond file
                return accumulator
            arg = int(arg)

            if inst == 'nop':
                pass
            elif inst == 'acc':
                accumulator += arg
            elif inst == 'jmp':
                i += arg - 1

            i += 1

        if not part2:
            return accumulator
        else:
            return None

    print('Part 1:', run_code(input_s))

    index_dict = {'nop': list(), 'acc': list(), 'jmp': list()}
    for i in range(len(input_s)):
        inst = input_s[i].split(' ')[0]
        index_dict[inst].append(i)

    found = False
    for swapi in index_dict['nop']:
        edited_code = list(input_s)
        edited_code[swapi] = 'jmp' + edited_code[swapi][3:]
        result = run_code(edited_code, part2=True)
        if result:
            print('Part 2:', result)
            found = True
            break

    if not found:
        for swapi in index_dict['jmp']:
            edited_code = list(input_s)
            edited_code[swapi] = 'nop' + edited_code[swapi][3:]
            result = run_code(edited_code, part2=True)
            if result:
                print('Part 2:', result)
                found = True
                break
