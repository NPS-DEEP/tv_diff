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
        group_pair = nodes[index1], nodes[index2]
        sd=float(row[2])
        edges[group_pair].append(sd)

# get groups
g = set()
for g1,g2 in edges.keys():
    g.add(g1)
groups = sorted(g)

with open("edge_cross_family_table_sd.tex", "w") as f:
    for i in range(len(groups)):
        l="%s&%d"%(groups[i],i+1)
        for j in range(len(groups)):
            if edges[groups[i],groups[j]]:
                l += "&%.1f"%statistics.mean(edges[groups[i],groups[j]])
            else:
                l += "&-"
        l += "\\\\"
        print(l, file=f)

