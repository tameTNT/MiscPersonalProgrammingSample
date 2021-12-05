from aocscrapper import get_AoC_input
from re import sub

if __name__ == '__main__':
    input_s = [passport.replace('\n', ' ') for passport in get_AoC_input(2020, 4).strip().split('\n\n')]
    input_s = [dict([tuple(details.split(':')) for details in passport.split(' ')]) for passport in input_s]

    def field_presence_check(key_set):
        if len({'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}.intersection(key_set)) == 7:
            return True


    valid_count = 0
    for passport in input_s:
        if field_presence_check(passport.keys()):
            valid_count += 1
    print('Part 1:', valid_count)

    valid_count = 0
    for passport in input_s:
        checks_passed = 0
        if field_presence_check(passport.keys()):
            if 1920 <= int(passport['byr']) <= 2002:
                checks_passed += 1

            if 2010 <= int(passport['iyr']) <= 2020:
                checks_passed += 1

            if 2020 <= int(passport['eyr']) <= 2030:
                checks_passed += 1

            if len(passport['hgt']) > 2:
                height = (int(passport['hgt'][:-2]), passport['hgt'][-2:])
                if height[1] == 'cm':
                    if 150 <= height[0] <= 193:
                        checks_passed += 1
                elif height[1] == 'in':
                    if 59 <= height[0] <= 76:
                        checks_passed += 1

            if passport['hcl'][0] == '#':
                # these are the only valid hexadecimal characters. removing these should leave only an empty string
                if len(sub('[abcdef0123456789]', '', passport['hcl'][1:])) == 0:
                    checks_passed += 1

            if passport['ecl'] in 'amb blu brn gry grn hzl oth'.split(' '):
                checks_passed += 1

            if len(passport['pid']) == 9:
                if str(int(passport['pid'])).zfill(9) == passport['pid']:
                    checks_passed += 1

            if checks_passed == 7:
                valid_count += 1

    print('Part 2:', valid_count)
