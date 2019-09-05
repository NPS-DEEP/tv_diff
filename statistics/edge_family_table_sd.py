#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1

#import pandas as pd
#import numpy as np
import csv
import statistics
from collections import defaultdict
from graph_paths import nodefile, edgefile

# nodes
# map node index to node family
# Id,Name,Group,Size,Modtime,MD5,SectionSize
nodes = dict()
with open(nodefile) as f:
    r=csv.reader(f)
    for row in r:
        index=row[0]
        if index.isdigit():
            group = row[2].replace("_","\_")
            nodes[int(index)] = group

# edges
# Source,Target,SD,Mean,Max,Sum

edges = defaultdict(list)
with open(edgefile) as f:
    r=csv.reader(f)
    for row in r:
        if not row[0].isdigit():
           continue

        index1 = int(row[0])
        index2 = int(row[1])
        if nodes[index1] == nodes[index2]:
            group = nodes[index1]
            sd = float(row[2])
            edges[group].append(sd)

num_edges = dict()
mins = dict()
maxs = dict()
means = dict()
group_sds = dict()

for group, sds in edges.items():
    num_edges[group] = len(sds)
    mins[group] = min(sds)
    maxs[group] = max(sds)
    means[group] = statistics.mean(sds)
    if num_edges[group] >= 2:
        group_sds[group] = statistics.stdev(sds)
    else:
        group_sds[group] = 0

with open("edge_family_table_sd.tex", "w") as f:

    for group in sorted(edges.keys()):
        # group, num_files, min size, max size, mean, SD
        print("%s&%d&%.1f&%.1f&%.1f&%.1f\\\\"%(group, num_edges[group],
                                           mins[group], maxs[group],
                                           means[group], group_sds[group]),
                                                              file=f)

