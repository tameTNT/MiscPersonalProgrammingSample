firewall = []
packet_index = -1
severity = 0


def reset_firewall():
    global firewall
    firewall = []
    with open("Inputs\\Day 13 Input.txt") as input_set:
        for line in input_set:
            data = line.strip().split(":")
            firewall.append([int(data[0]), int(data[1]), 0, "S"])


reset_firewall()
depths = [data[0] for data in firewall]

for delay in range(1000):
    for i in range(max(depths) + 1 + delay):
        if i >= delay:
            packet_index += 1

        for wall in firewall:
            depth = wall[0]
            range_ = wall[1]

            if depth == packet_index and wall[2] == 0:
                severity += depth * range_

            if wall[3] == "S":
                wall[2] += 1
            elif wall[3] == "N":
                wall[2] -= 1

            if wall[2] == 0:
                wall[3] = "S"
            elif wall[2] == range_ - 1:
                wall[3] = "N"

    if severity == 0:
        print(delay)
        break
    else:
        packet_index = -1
        severity = 0
        reset_firewall()
