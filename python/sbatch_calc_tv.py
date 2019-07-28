#!/usr/bin/env python3
import glob, json
from os.path import exists
from argparse import ArgumentParser

from calc_tv import calc_tv

# main
if __name__=="__main__":
    glob_path="/smallwork/bdallen/executable_files/*/*.tmp"

    # args
    parser = ArgumentParser(prog='sbatch_calc_tv.py',
                   description="Generate TV files for glob.")
    parser.add_argument("slice_index", type=int, help="Slice number to work on")
    parser.add_argument("-f", "--file_glob", type=str,
                        default=glob_path,
                        help="bash-syntax glob of files to compare")
    parser.add_argument("-s", "--section_size", type=int, default=500,
                 help="The section size of the texture sample, default 500.")
    args = parser.parse_args()

    # files
    files = glob.glob(args.file_glob)
    print("Processing %d files..."%len(files))

    infile = files[args.slice_index-1]
    outfile = "%s.tv"%infile

    if exists(outfile):
        print("Skipping existing file '%s'"%outfile)
    else:
        print("Processing file '%s'"%infile)
        calc_tv(infile, outfile, args.section_size)

    print("Done.")
