#!/usr/bin/env python3
# https://stackoverflow.com/questions/29672375/histogram-in-matplotlib-time-on-x-axis

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
from graph_paths import nodefile

data = list()

# iterate rows of csv
with open(nodefile) as f:
    r=csv.reader(f)
    for row in r:
        c=row[4]
        if c.isdigit():
            data.append(int(c))

# convert the epoch format to matplotlib date format 
mpl_data = mdates.epoch2num(data)

fig, ax = plt.subplots(1,1)
ax.hist(mpl_data, bins=50, edgecolor='black')

locator = mdates.AutoDateLocator()
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(mdates.AutoDateFormatter(locator))

plt.title("Number of files by modification time")
plt.ylabel("Number of files")
plt.xlabel("Modification time")
#plt.show()
plt.savefig("node_hist_by_time.pdf")

