#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1

from os.path import join, expanduser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from graph_paths import edgefile

x = list()

# Source,Target,SD,Mean,Max,Sum
# ,,,,,,Combinations from /smallwork/bdallen/tv_files/*.tv
# ,,,,,,1294 files, 836571 combinations

# iterate rows of csv
with open(edgefile) as f:
    r=csv.reader(f)
    for row in r:
        try:
            x.append(int(row[4])/int(row[5]))
        except ValueError:
            pass

print("count: %d, total: %f"%(len(x), sum(x)))

x = pd.Series(x)

#logbins = np.logspace(0,.0010,50)
#plt.hist(x, log=True, bins=logbins, edgecolor="black")
#plt.hist(x, bins=logbins, edgecolor="black")
plt.hist(x, bins=50, edgecolor="black")
#plt.xscale('log')
plt.yscale('log')
plt.title("Number of matches by Max/Sum similarity")
plt.xlabel("Similarity measure in Max/Sum")
plt.ylabel("Number of matches")
#plt.grid(True)
#plt.show()
plt.savefig("edge_hist_sim_by_ratio.pdf")

