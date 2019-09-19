#!/usr/bin/env python3.6

import os, glob, hashlib

def get_relevant_md5s(files):
    file_md5s = dict()
    for f in files:
        md5 = hashlib.md5(open(f, "rb").read()).hexdigest().upper()
        print("relevant md5: %s"%md5)
        file_md5s[f] = md5
    return file_md5s

def maybe_set_modtime(md5, modtime, md5_modtimes):
    if modtime < 300000000:
        print("low modtime: %d"%modtime)
        return
    if md5 in md5_modtimes and modtime > md5_modtimes[md5]:
        return
    print("setting modtime")
    md5_modtimes[md5] = modtime


def get_md5_modtimes(bigtable_file, relevant_md5s):
    md5_modtimes = dict()  # key=md5, value=modtime
    with open(bigtable_file) as f:
        i=1
        while True:
            line = f.readline().strip()
            if not line:
                break
            md5 = line[41:73]
            if md5 in relevant_md5s:
                parts = line.split("|")
                modtime = int(parts[14])
                maybe_set_modtime(md5, modtime, md5_modtimes)
            i+=1
            if i%1000000 == 0:
                print(i)
    return md5_modtimes

def set_modtimes(file_md5s, md5_modtimes):
    for f, md5 in file_md5s.items():
        if md5 in md5_modtimes:
            modtime = md5_modtimes[md5]
            print("set %d for file %s"%(modtime, f))
            os.utime(f, (modtime, modtime))
        else:
            print("no modtime for file %s"%f)

if __name__=="__main__":
    files = glob.glob("/smallwork/bdallen/executable_files/*/*.tmp")
    bigtable_file = "bigtable.out"
    print("get md5s...")
    file_md5s = get_relevant_md5s(files)
    relevant_md5s = set()
    for md5 in file_md5s.values():
        relevant_md5s.add(md5)
    print("get md5 modtimes...")
    md5_modtimes = get_md5_modtimes(bigtable_file, relevant_md5s)
    print("set md5 modtimes...")
    set_modtimes(file_md5s, md5_modtimes)
    print("Done.")

