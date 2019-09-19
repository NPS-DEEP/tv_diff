#!/usr/bin/env python3.6
import os, glob, json, shutil
from os.path import exists, getsize

if __name__=="__main__":
#    glob_path_from_neil="/smallwork/bdallen/executable_files_from_neil/*/*.tmp"
    glob_path_from_neil="/home/bdallen/executable_files_neil/*/*.tmp"
    dest_path_tv_500="/smallwork/bdallen/tv_files_500/*.tv"

    total = 0
    gt1M = 0
    lt1K = 0
    in_range = 0

    files = glob.glob(glob_path_from_neil)
    for f in files:
        total += 1
        size = getsize(f)
        if size > 1000000:
            gt1M += 1
        elif size < 1000:
            lt1K += 1
        else:
            in_range += 1

    files = glob.glob(dest_path_tv_500)
    unique_in_range = len(files)

    print("All files: %d"%total)
    print("Files>1M: %d"%gt1M)
    print("Files<1K: %d"%lt1K)
    print("Files in range: %d"%in_range)
    print("Unique files in range: %d"%unique_in_range)

