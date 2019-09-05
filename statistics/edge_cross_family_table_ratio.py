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
        name1=nodes[int(row[0])]
        name2=nodes[int(row[1])]
#        if name1<name2:
#            name1,name2=name2,name1
        ratio=float(row[4])/float(row[5])
        edges[name1,name2].append(ratio)
        edges[name2,name1].append(ratio)

# get groups
g = set()
for g1,_g2 in edges.keys():
    g.add(g1)
groups = sorted(g)
if len(groups) != 24:
   raise RuntimeError("bad")

with open("edge_cross_family_table_ratio.tex", "w") as f:
    # left half
    print("\\textbf{Family} & \\textbf{n} "
          "& \\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} "
          "& \\textbf{5} & \\textbf{6} & \\textbf{7} & \\textbf{8} ",
          "& \\textbf{9} & \\textbf{10} & \\textbf{11} & \\textbf{12}\\\\", file=f)
    print("\\hline", file=f)
    for i in range(24):
        l="%s&%d"%(groups[i],i+1)
        for j in range(12):
            if edges[groups[i],groups[j]]:
                l += "&%.3f"%statistics.mean(edges[groups[i],groups[j]])
            else:
                l += "&-"
        l += "\\\\"
        print(l, file=f)

    # right half
    print("\\hline", file=f)
    print("\\hline", file=f)
    print("\\textbf{Family} & \\textbf{n} "
          "& \\textbf{13} & \\textbf{14} & \\textbf{15} & \\textbf{16} "
          "& \\textbf{17} & \\textbf{18} & \\textbf{19} & \\textbf{20} "
          "& \\textbf{21} & \\textbf{22} & \\textbf{23} & \\textbf{24}\\\\", file=f)
    print("\\hline", file=f)
    for i in range(24):
        l="%s&%d"%(groups[i],i+1)
        for j in range(12,24):
            if edges[groups[i],groups[j]]:
                l += "&%.3f"%statistics.mean(edges[groups[i],groups[j]])
            else:
                l += "&-"
        l += "\\\\"
        print(l, file=f)

