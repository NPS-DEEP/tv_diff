#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1

from os.path import join, expanduser
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from graph_paths import edgefile

x_sd = list()
x_ratio = list()

# Source,Target,SD,Mean,Max,Sum
# ,,,,,,Combinations from /smallwork/bdallen/tv_files/*.tv
# ,,,,,,1294 files, 836571 combinations

# iterate rows of csv
with open(edgefile) as f:
    r=csv.reader(f)
    for row in r:
        try:
            x_sd.append(float(row[2]))
            x_ratio.append(int(row[4])/int(row[5]))
        except ValueError:
            pass

if len(x_sd) != len(x_ratio):
    raise(RuntimeError("Bad"))

print("count: %d:"%len(x_sd))

x_sd = pd.Series(x_sd)
x_ratio = pd.Series(x_ratio)

fig, (ax1,ax2) = plt.subplots(1,2)
fig.suptitle("Similarity matches by Standard Deviation (SD) and Max/Sum")

logbins1 = np.logspace(0,2.5,50)
ax1.hist(x_sd, bins=logbins1, edgecolor="black")
#ax1.hist(x_sd, log=True, bins=logbins1, edgecolor="black")
#zax1.xscale('log')
ax1.set_title("Matches by SD")
ax1.set(xlabel="Similarity measure in SD",
        ylabel="Number of similarity matches",
        xscale="log")

#logbins2 = np.logspace(0,.001,50)
#ax2.hist(x_ratio, bins=logbins1, edgecolor="black")
ax2.hist(x_ratio, bins=50, edgecolor="black")
#ax2.hist(x_ratio, log=True, bins=logbins1, edgecolor="black")
ax2.set_title("Matches by Max/Sum")
ax2.set(xlabel="Similarity measure in Max/Sum",
        yscale="log")

#plt.grid(True)
#plt.show()
plt.savefig("edge_hist_sim.pdf")

