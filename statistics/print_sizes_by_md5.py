#!/usr/bin/env python3.6
# run on Grace to find unique file count and large files

import os, glob, hashlib

if __name__=="__main__":
    files = glob.glob("/home/bdallen/work/executable_files_neil/*/*.tmp")
#    files = glob.glob("/smallwork/bdallen/executable_files/*/*.tmp")
    names_by_md5 = dict()
    sizes_by_md5 = dict()
    count = 0
    for f in files:
        count += 1
        md5 = hashlib.md5(open(f, "rb").read()).hexdigest().upper()
        names_by_md5[md5] = f
        size = os.stat(f).st_size
        sizes_by_md5[md5] = size

    # count
    print("file count: %d, md5 %d: "%(count, len(sizes_by_md5)))

    # sizes
    count_smaller = 0
    count_greater = 0
    for key, value in sizes_by_md5.items():
        if value <= 34969111:
            count_smaller += 1
        else:
            count_greater += 1
            print("Large file: %s, %d, %s"%(key, value, names_by_md5[key]))
#        print("%s, %d, %s"%(key, value, names_by_md5[key]))
    print("size <= 3496911: %d, count greater: %d"%(count_smaller, count_greater))
    print("done.")
