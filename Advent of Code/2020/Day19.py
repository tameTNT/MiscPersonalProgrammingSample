from aocscrapper import get_AoC_input
import regex as re  # extended regex library needed for recursion functionality - '(?&self)?'

if __name__ == '__main__':
    rules, messages = [x.strip().split('\n') for x in get_AoC_input(2020, 19, get_test=False).strip().split('\n\n')]

    rule_dict = {r.split(': ')[0]: r.split(': ')[1].replace('"', '') for r in rules}

    def build_rule(rule_d):
        re_rule = f" {rule_d['0']} "
        while re.match(r'.* \d+ .*', re_rule):  # while there is a number with padding spaces in the string somewhere
            rules_to_fill = set(re.findall(r' (\d+) ', re_rule))  # finds all rules that still need to be filled in
            for rule_num in rules_to_fill:
                if f' {rule_num} ' in f' {rule_d[rule_num]} ':  # a recursive rule
                    # These solutions are hacky and hard coded for the solutions needed - not for general case
                    # 11: 42 31 | 42 11 31
                    # 8: 42 | 42 8
                    sub_rules = rule_d[rule_num].split(' | ')[0].split(' ')
                    recursive_replace = str()

                    # for i in range(1, 6):  # this limits the recursion depth to 6 (but at least 1). Larger numbers take even longer to run
                    #     recursive_replace += '('
                    #     for sub in sub_rules:
                    #         recursive_replace += f' ( {rule_d[sub]} ){{{i}}} '  # {{ to escape { character in f-string
                    #     recursive_replace += ') | '
                    # recursive_replace = recursive_replace[:-2]  # remove trailing pipe character

                    if len(sub_rules) == 2:
                        # ?P<...> labels group while (?&...)? reuses the group recursively
                        # Help from https://www.reddit.com/r/adventofcode/comments/kg1mro/2020_day_19_solutions/ggc6oay
                        recursive_replace = f'(?P<self> {sub_rules[0]} (?&self)? {sub_rules[1]} )'
                    elif len(sub_rules) == 1:
                        recursive_replace = f' ( {sub_rules[0]} )+ '

                    re_rule = re_rule.replace(f' {rule_num} ', f' ({recursive_replace}) ')

                else:
                    re_rule = re_rule.replace(f' {rule_num} ', f' ( {rule_d[rule_num]} ) ')

        return f"^{re_rule.replace(' ', '')}$"  # ensures there aren't any trailing characters (which would be invalid) and removes whitesapce

    def count_matches(message_l, r):
        message_match_count = 0
        for message in message_l:
            if re.match(r, message):
                message_match_count += 1
        return message_match_count

    print('Part 1:', count_matches(messages, build_rule(rule_dict)))

    rule_dict['8'] = '42 | 42 8'
    rule_dict['11'] = '42 31 | 42 11 31'
    print('Part 2:', count_matches(messages, build_rule(rule_dict)))
