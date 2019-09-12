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

edges_dict = defaultdict(list)
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
            ratio = float(row[4])/float(row[5])
            edges_dict[group].append((sd, ratio))

with open("edge_family_statistics_table.tex", "w") as f:

    for group in sorted(edges_dict.keys()):
        edges = edges_dict[group]
        num_edges = len(edges)
        sds = [row[0] for row in edges]
        ratios = [row[1] for row in edges]
        sd_mins = min(sds)
        ratio_mins = min(ratios)
        sd_maxs = max(sds)
        ratio_maxs = max(ratios)
        sd_means = statistics.mean(sds)
        ratio_means = statistics.mean(ratios)
        if num_edges >= 2:
            sd_group_sds = statistics.stdev(sds)
            ratio_group_sds = statistics.stdev(ratios)
        else:
            sd_group_sds = 0
            ratio_group_sds = 0

        # group, num_edges, min SD, max SD, mean SD, SD SD,
        #                   min ratio, max ratio, mean ratio, SD ratio
        print("%s&%d&%.1f&%.1f&%.1f&%.1f&"
                    "%.3f&%.3f&%.3f&%.3f\\\\"%(group, num_edges,
              sd_mins, sd_maxs, sd_means, sd_group_sds,
              ratio_mins, ratio_maxs, ratio_means, ratio_group_sds),
                                                              file=f)

