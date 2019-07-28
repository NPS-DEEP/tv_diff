#!/usr/bin/env python3.6
import os, glob, json, shutil
from os.path import exists

def do_copy(tv_filename, dest_dir):

        with open(tv_filename) as infile:
            tv_data = json.load(infile)

        file_md5 = tv_data["md5"]

        shutil.copy(tv_filename, os.path.join(dest_dir, "%s.tv"%file_md5))

if __name__=="__main__":
    glob_path="/smallwork/bdallen/executable_files/*/*.tv"
    dest_dir = "/smallwork/bdallen/tv_files"

    files = glob.glob(glob_path)

    i=0
    for f in files:
        i+=1
        print("%d of %d  %s"%(i, len(files), f))
        do_copy(f, dest_dir)

    print("Done.")

