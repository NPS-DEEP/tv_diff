#!/usr/bin/env python3.6
import os, glob
from os.path import getsize

if __name__=="__main__":
    glob_path_500="/smallwork/bdallen/executable_files_500/*/*.tmp"
    glob_path_1000="/smallwork/bdallen/executable_files_1000/*/*.tmp"

    paths = [
             glob_path_500,
             glob_path_1000,
            ]

    for path in paths:
        files = glob.glob(path)
        for file in files:
            size = getsize(file)
            if size > 5000000 or size < 1000:
                print("size %d file %s"%(size, file))
                os.remove(file)

