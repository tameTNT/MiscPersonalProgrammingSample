judge_total = 0
genA = 703
genB = 516
pair = [0,0]


def create_values():
    global genA, genB
    genA *= 16807
    genA %= 2147483647
    genB *= 48271
    genB %= 2147483647

    pair[0], pair[1] = bin(genA), bin(genB)


for i in range(40000000):
    create_values()
    if pair[0][-16:] == pair[1][-16:]:
        judge_total += 1

print(judge_total)
