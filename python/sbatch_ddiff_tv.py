#!/usr/bin/env python3
import os, sys, glob, itertools, hashlib
import json
from os.path import expanduser, exists
from argparse import ArgumentParser

from settings_store import read_settings
from read_tv_file import read_tv_file
from similarity_math import generate_similarity_data

def _total_combinations(files):
    # hack to get total
    total = 0
    for _,_ in itertools.combinations(range(1, len(files)+1), 2):
        total += 1
    return total

def show_node_data(settings, files, f):

    # column names
    print("Id,Name,Group,Size,Modtime,MD5,SectionSize", file=f)

    # metadata
    print(",,,,,,,Combinations from %s"%args.file_glob, file=f)
    print(",,,,,,,%d files, %d combinations"%(len(files),
                                      _total_combinations(files)), file=f)

    for i in range(1, len(files)+1):
        tv_filename = files[i-1]
        with open(tv_filename) as infile:
            tv_data = json.load(infile)

        filename = tv_data["filename"]
        file_group = tv_data["file_group"]
        file_size = tv_data["file_size"]
        file_modtime = tv_data["file_modtime"]
        file_md5 = tv_data["md5"]
        section_size = tv_data["section_size"]

        print("%d,%s,%s,%d,%d,%s,%d"%(i, filename, file_group, file_size,
                                file_modtime, file_md5, section_size), file=f)

def show_similarity_histogram_data(files, step, settings, slice_index, f):
    # get combinations of files as file_pairs
    tv_data1 = {"filename":""}
    file_pairs = itertools.combinations(range(1, len(files)+1), 2)
    for n1, n2 in file_pairs:

        # only process this slice index
        if n1 != slice_index:
            continue

        file1 = files[n1-1]
        file2 = files[n2-1]

        # get data, allow cache on file1
        if file1 != tv_data1["filename"]:
            tv_data1 = read_tv_file(file1)
        tv_data2 = read_tv_file(file2)

        # calculate similarity data
        d = generate_similarity_data(tv_data1, tv_data2, args.step_granularity,
                                     settings, False)

        # skip no correlation
        if not d["sd"]:
            continue

        # directed
        # Source,Target,sd,mean,max,sum
        if tv_data1["file_modtime"] < tv_data2["file_modtime"]:
            a=n1
            b=n2
        else:
            a=n2
            b=n1
        print("%d,%d,%.4f,%.4f,%d,%d"%(
              a,b,d["sd"],d["mean"],d["max"],d["sum"]), file=f)

# main
if __name__=="__main__":

    glob_path = "/smallwork/bdallen/tv_files/*.tv"

    # args
    default_settings_file = os.path.join(expanduser("~"),
                                         ".tv_threshold_settings")
    parser = ArgumentParser(prog='sbatch_ddiff_tv.py',
                   description="Get histogram diff for sbatch glob.")
    parser.add_argument("slice_index", type=int, help="Slice number to work on")
    parser.add_argument("-f", "--file_glob", type=str,
                        default=glob_path,
                        help="bash-syntax glob of files to compare")
    parser.add_argument("-o", "--outfile_prefix", type=str,
                        default="sbatch_ddiff_tv_",
                        help="output csv files with node.csv or "
                             "edge_<slice index>.csv appended")
    parser.add_argument("-t", "--tv_threshold_settings_file", type=str,
                        default=default_settings_file,
                        help="texture vector threshold settings file to use")
    parser.add_argument("-s", "--step_granularity", type=int, default=1,
                        help="step granularity optimization")
    parser.add_argument("-n", "--show_node_data", action="store_true",
                        help="show node data only and stop")
    args = parser.parse_args()

    # files and file pairs
    files = glob.glob(args.file_glob)
    print("Processing %d files slice %d..."%(len(files), args.slice_index))
    settings = read_settings(args.tv_threshold_settings_file)

    # nodes only
    if args.show_node_data:
        show_node_data(settings, files, sys.stdout)
        exit(0)

    else:
        # nodes
        if args.slice_index == 1:
            node_filename = "%snode.csv"%(args.outfile_prefix)
            with open(node_filename, "w") as f:
                show_node_data(settings, files, f)

        # edges
        edge_filename = "%sedge_%d.csv"%(args.outfile_prefix, args.slice_index)
        with open(edge_filename, "w") as f:
            if args.slice_index == 1:
                print("Source,Target,SD,Mean,Max,Sum", file=f)
                print(",,,,,,Combinations from %s"%args.file_glob, file=f)
                print(",,,,,,%d files, %d combinations"%(len(files),
                                      _total_combinations(files)), file=f)
            show_similarity_histogram_data(files, args.step_granularity,
                                           settings, args.slice_index, f)

    print("Done processing slice %d."%args.slice_index)

