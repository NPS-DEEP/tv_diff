#!/usr/bin/env python3
# https://stackoverflow.com/questions/47850202/plotting-a-histogram-on-a-log-scale-with-matplotlib?rq=1
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from graph_paths import nodefile

x = list()

# iterate rows of csv
with open(nodefile) as f:
    r=csv.reader(f)
    for row in r:
        c=row[3]
        if c.isdigit():
            x.append(int(c))

x = pd.Series(x)

logbins = np.logspace(4,6,50)
plt.hist(x, bins=logbins, edgecolor="black")
plt.xscale('log')
plt.title("Number of files by file size")
plt.ylabel("Number of files")
plt.xlabel("File size in bytes")
#plt.grid(True)
#plt.show()
plt.savefig("node_hist_by_size.pdf")

