#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1

from os.path import join, expanduser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from graph_paths import edgefile

x_sd = list()

# Source,Target,SD,Mean,Max,Sum
# ,,,,,,Combinations from /smallwork/bdallen/tv_files/*.tv
# ,,,,,,1294 files, 836571 combinations

# iterate rows of csv
with open(edgefile) as f:
    r=csv.reader(f)
    for row in r:
        try:
            x_sd.append(float(row[2]))
        except ValueError:
            pass

print("count: %d:"%len(x_sd))

x_sd = pd.Series(x_sd)

logbins = np.logspace(0,2.5,50)
plt.hist(x_sd, bins=logbins, edgecolor="black")
plt.xscale('log')
plt.title("File similarity across all files")
plt.xlabel("Similarity measure")
plt.ylabel("Number of similarity matches")

#plt.grid(True)
#plt.show()
plt.savefig("edge_hist_sim.pdf")

