firewall = []
packet_index = -1
severity = 0

with open("Inputs\\Day 13 Input.txt") as input_set:
    for line in input_set:
        data = line.strip().split(":")
        firewall.append([int(data[0]), int(data[1]), 0, "S"])

depths = [wall[0] for wall in firewall]

for i in range(max(depths)+1):
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

print(severity)
