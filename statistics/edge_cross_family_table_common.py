#import pandas as pd
#import numpy as np
import csv
import statistics
from collections import defaultdict
from graph_paths import nodefile, edgefile

def edge_cross_family_table_common(mode, outfile):

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
            if mode == "sd":
                sd=float(row[2])
                edges[name1,name2].append(sd)
                edges[name2,name1].append(sd)
            elif mode == "ratio":
                ratio=float(row[4])/float(row[5])
                edges[name1,name2].append(ratio)
                edges[name2,name1].append(ratio)
            else:
                raise RuntimeError("bad")


    # get groups
    g = set()
    for g1,_g2 in edges.keys():
        g.add(g1)
    groups = sorted(g)
    if len(groups) != 23:
       raise RuntimeError("bad: %d"%len(groups))

    with open(outfile, "w") as f:
        # left half
        print("\\begin{tabular}{|l|r|r|r|r|r|r|r|r|r|r|r|r|r|}", file=f)
        print("\\hline \\hline", file=f)
        print("\\textbf{Family} & \\textbf{n} "
              "& \\textbf{1} & \\textbf{2} & \\textbf{3} & \\textbf{4} "
              "& \\textbf{5} & \\textbf{6} & \\textbf{7} & \\textbf{8} ",
              "& \\textbf{9} & \\textbf{10} & \\textbf{11} & \\textbf{12}\\\\",
                                                                  file=f)
        print("\\hline", file=f)
        for i in range(23):
            l="%s&%d"%(groups[i],i+1)
            for j in range(12):
                if edges[groups[i],groups[j]]:
                    if mode == "sd":
                        l += "&%.1f"%statistics.mean(edges[groups[i],groups[j]])
                    elif mode == "ratio":
                        l += "&%.2f"%statistics.mean(edges[groups[i],groups[j]])
                    else:
                        raise RuntimeError("bad")
                else:
                    l += "&-"
            l += "\\\\"
            print(l, file=f)
        print("\\hline", file=f)
        print("\\end{tabular}", file=f)

        # right half
        print("\\begin{tabular}{|l|r|r|r|r|r|r|r|r|r|r|r|r|}", file=f)
        print("\\hline", file=f)
        print("\\hline", file=f)
        print("\\textbf{Family} & \\textbf{n} "
              "& \\textbf{13} & \\textbf{14} & \\textbf{15} & \\textbf{16} "
              "& \\textbf{17} & \\textbf{18} & \\textbf{19} & \\textbf{20} "
              "& \\textbf{21} & \\textbf{22} & \\textbf{23}\\\\", file=f)
        print("\\hline", file=f)
        for i in range(23):
            l="%s&%d"%(groups[i],i+1)
            for j in range(12,23):
                if edges[groups[i],groups[j]]:
                    if mode == "sd":
                        l += "&%.1f"%statistics.mean(edges[groups[i],groups[j]])
                    elif mode == "ratio":
                        l += "&%.2f"%statistics.mean(edges[groups[i],groups[j]])
                    else:
                        raise RuntimeError("bad")
                else:
                    l += "&-"
            l += "\\\\"
            print(l, file=f)
        print("\\hline", file=f)
        print("\\end{tabular}", file=f)

