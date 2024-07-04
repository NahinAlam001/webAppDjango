#!/usr/bin/env python3

import json

BUSES = (1, 2, 3, 6, 8)
# data = []
data: dict[str, dict] = {}

for _ in range(int(input())):
    line = input()
    tokens = line.split(", ")
    time = tokens[0].strip()
    tokens = tokens[1:]
    data_at_this_time = {}
    # for i, bus in enumerate(BUSES):
    #     data_at_this_time[bus] = {
    #         "angle": tokens[i * 2].strip(),
    #         "voltage": tokens[i * 2 + 1].strip(),
    #     }
    # data.append({
    #     "time": time,
    #     "data": data_at_this_time,
    # })
    for i, bus in enumerate(BUSES):
        data_at_this_time[bus] = {
            "angle": tokens[i * 2],
            "voltage": tokens[i * 2 + 1],
        }
    data[time] = data_at_this_time

with open("src/lib/gen_watch.json", "w") as f:
    # f.write(str(data))
    json.dump(data, f, indent=2)
