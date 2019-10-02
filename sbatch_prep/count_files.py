#!/usr/bin/env python3.6
import os, glob, json, shutil
from os.path import exists

if __name__=="__main__":
    glob_path_neil="/home/bdallen/work/executable_files_neil/*/*.tmp"
    glob_path_from_neil="/smallwork/bdallen/executable_files_from_neil/*/*.tmp"
    glob_path_tv_from_neil="/smallwork/bdallen/executable_files_from_neil/*/*.tv"
    glob_path_500="/smallwork/bdallen/executable_files_500/*/*.tmp"
    glob_path_512="/smallwork/bdallen/executable_files_512/*/*.tmp"
    glob_path_tv_500="/smallwork/bdallen/executable_files_500/*/*.tv"
    glob_path_tv_512="/smallwork/bdallen/executable_files_512/*/*.tv"
    dest_path_tv_500="/smallwork/bdallen/tv_files_500/*.tv"
    dest_path_tv_512="/smallwork/bdallen/tv_files_500/*.tv"

    paths = [
             glob_path_neil,
             glob_path_from_neil,
             glob_path_tv_from_neil,
             glob_path_500,
             glob_path_tv_500,
             dest_path_tv_500,
             glob_path_512,
             glob_path_tv_512,
             dest_path_tv_512,
            ]

    for path in paths:
        files = glob.glob(path)
        print("count for %s: %d"%(path, len(files)))

