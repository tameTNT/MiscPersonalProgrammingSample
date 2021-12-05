import operator
import collections

with open("Inputs\\Day4.txt", "r") as input_set:
    guard_total_time_asleep = dict()
    guard_times = dict()

    ordered_list = sorted([line.strip() for line in input_set])

    current_guard = int()
    asleep_from = int()

    for record in ordered_list:
        minutes = int(record.split(" ")[1].split(":")[1].strip("]"))
        # print(record, minutes)
        if "#" in record:
            current_guard = int(record.split("#")[1].split(" ")[0])
            if current_guard not in guard_total_time_asleep:
                guard_total_time_asleep[current_guard] = 0
                guard_times[current_guard] = list()

        if "falls asleep" in record:
            asleep_from = minutes

        if "wakes up" in record:
            time_asleep = minutes - asleep_from
            guard_total_time_asleep[current_guard] += time_asleep
            for i in range(time_asleep):
                guard_times[current_guard].append(asleep_from + i)

    sleepiest_guard = max(guard_total_time_asleep.items(), key=operator.itemgetter(1))[0]  # Ignore error
    print("Part 1: ", collections.Counter(guard_times[sleepiest_guard]).most_common(1)[0][0] * sleepiest_guard)

    most_minutes_dict = dict()
    for guard in guard_times.keys():
        if guard_times[guard] != list():  # Needed to eliminate this one empty guard in the dictionary
            most_minutes_dict[guard] = collections.Counter(guard_times[guard]).most_common(1)[0][1]

    guard_same_min_asleep = max(most_minutes_dict.items(), key=operator.itemgetter(1))[0]
    print("Part 2: ",
          guard_same_min_asleep * collections.Counter(guard_times[guard_same_min_asleep]).most_common(1)[0][0])
