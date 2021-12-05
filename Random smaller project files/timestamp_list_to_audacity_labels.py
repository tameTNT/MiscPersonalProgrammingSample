import re

print("Paste YouTube string (sep by newline) into youtube_timestamp.txt")
youtube_timestamps = open("youtube_timestamp.txt", "r+").read().strip().split("\n")
re_format = input("Input line format (e.g. '%M:%S %title'): ")
re_format = re_format.replace("%M", r"(?P<min>\d\d)").replace("%S", r"(?P<sec>\d\d)").replace("%title", r"(?P<title>.*)")

with open("output_labels.txt", "w+", encoding="UTF-8") as fobj:
    for t in youtube_timestamps:
        matches = re.match(re_format, t)
        values = matches.groupdict()
        time_s = int(values['min'])*60 + int(values['sec'])
        fobj.write(f"{time_s}.000000\u0009{time_s}.000000\u0009{values['title']}\n")
    fobj.close()

print("Output to output_labels.txt")
