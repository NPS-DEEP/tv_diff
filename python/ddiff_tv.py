#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
import statistics
from settings_store import read_settings, default_settings_file, \
                           texture_compatible
from similarity_math import generate_similarity_data
from read_tv_file import read_tv_file

# main
if __name__=="__main__":
    # args
    parser = ArgumentParser(prog='ddiff_tv.py',
                            description="Get data difference histogram "
                                        "statistics between two files.")
    parser.add_argument("file1", type=str, help="TV input file 1")
    parser.add_argument("file2", type=str, help="TV input file 2")
    parser.add_argument("-t", "--tv_threshold_settings_file", type=str,
                        default=default_settings_file,
                        help="texture vector threshold settings file to use")
    parser.add_argument("-s", "--step_granularity", type=int, default=1,
                        help="step granularity optimization")
    args = parser.parse_args()

    # settings
    settings = read_settings(args.tv_threshold_settings_file)
    print("Settings:")
    print(settings)

    # file pair
    tv_data1 = read_tv_file(args.file1)
    tv_data2 = read_tv_file(args.file2)

    # file information
    print("File 1: %s  %s"%(tv_data1["md5"], tv_data1["filename"]))
    print("File 2: %s  %s"%(tv_data2["md5"], tv_data2["filename"]))

    # statistics
    d = generate_similarity_data(tv_data1, tv_data2, args.step_granularity,
                                 settings, False)

    print("SD: %.4f, mean: %.4f, max: %d, sum: %d"%(
                               d["sd"], d["mean"], d["max"], d["sum"]))

