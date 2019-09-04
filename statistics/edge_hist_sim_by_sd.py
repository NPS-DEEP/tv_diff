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
        c=row[2]
        try:
            x.append(float(c))
        except ValueError:
            pass

print("count: %d, total: %f"%(len(x), sum(x)))

x = pd.Series(x)

logbins = np.logspace(0,2.5,50)
#plt.hist(x, log=True, bins=logbins, edgecolor="black")
plt.hist(x, bins=logbins, edgecolor="black")
plt.xscale('log')
plt.title("Number of matches by SD similarity")
plt.xlabel("Similarity measure in SD")
plt.ylabel("Number of matches")
#plt.grid(True)
#plt.show()
plt.savefig("edge_hist_sim_by_sd.pdf")

