#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics
import csv
from graph_paths import nodefile
from collections import defaultdict

files = defaultdict(list)

# iterate rows of csv
with open(nodefile) as f:
    r=csv.reader(f)
    for row in r:
        size=row[3]
        if size.isdigit():
            group = row[2].replace("_","\_")
            files[group].append(int(size))

num_files = dict()
mins = dict()
maxs = dict()
means = dict()
sds = dict()

total = 0
for group, sizes in files.items():
    total += len(sizes)
    num_files[group] = len(sizes)
    mins[group] = min(sizes)
    maxs[group] = max(sizes)
    means[group] = statistics.mean(sizes)
    sds[group] = statistics.stdev(sizes)

with open("node_family_table.tex", "w") as f:

    for group in sorted(files.keys()):
        # group, num_files, min size, max size, mean, SD
        print("%s&%d&%d&%d&%.1f&%.1f\\\\"%(group, num_files[group],
                                           mins[group], maxs[group],
                                           means[group], sds[group]), file=f)

print("total: %d"%total)


