# As this program takes a while to run, when finished it makes a sound to alert the user therefore winsound is needed
import winsound

judge_total = 0
genA = 703
genB = 516
genA_pair_count = 0
genB_pair_count = 0
A_approved = []
B_approved = []


def create_values():
    global genA, genB, genA_pair_count, genB_pair_count, A_approved, B_approved
    if genA_pair_count < 5000000:
        genA *= 16807
        genA %= 2147483647
        if genA % 4 == 0:
            A_approved.append(bin(genA)[-16:])
            genA_pair_count += 1

    if genB_pair_count < 5000000:
        genB *= 48271
        genB %= 2147483647
        if genB % 8 == 0:
            B_approved.append(bin(genB)[-16:])
            genB_pair_count += 1


while True:
    create_values()
    if genA_pair_count == 5000000 and genB_pair_count == 5000000:
        break

for i in range(genA_pair_count):
    if A_approved[i] == B_approved[i]:
        judge_total += 1
print(judge_total)

winsound.Beep(440, 1000)
