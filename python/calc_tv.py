#!/usr/bin/env python3
# requires numpy: "sudo pip3 install numpy"

import sys, os, hashlib
from argparse import ArgumentParser
import numpy as np
import json
from math import e, log
from version_file import VERSION

texture_names=("sd","mean","mode","mode_count","entropy")

# use _entropy2 instead
def _shannon2_entropy(b):
    # https://stackoverflow.com/questions/42683287/python-numpy-shannon-
    # entropy-array?rq=1
    b_sum = b.sum()
    if b_sum == 0:
        return 0
    p=b/b.sum()
    print(np.log2(p))
    shannon2=-np.sum(p*np.log2(p))
    return shannon2.item()

# from https://stackoverflow.com/questions/15450192/fastest-way-to-compu
# te-entropy-in-python approach 2
def _entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value,counts = np.unique(labels, return_counts=True)
  probs = counts / n_labels
  n_classes = np.count_nonzero(probs)

  if n_classes <= 1:
    return 0

  ent = 0.

  # Compute entropy
  base = e if base is None else base
  for i in probs:
    ent -= i * log(i, base)

  # quick observation shows ent between 0.0 and 4.0.
  return ent

def _texture_vector(b, section_size):
    # try to normalize for 0 to 255 values
    sd = np.std(b).item() * 2                       # standard deviation
    mean = np.mean(b).item()                        # mean
    # https://stackoverflow.com/questions/6252280/find-the-most-frequent
    #-number-in-a-numpy-vector
    mode = np.argmax(np.bincount(b)).item()         # mode
    mode_count = list(b).count(mode) * (256.0/section_size) # mode_count
#    entropy = _shannon2_entropy(b)                   # entropy
    entropy = round(_entropy2(b)*43)                # entropy
   
    return (sd, mean, mode, mode_count, entropy)

def calc_tv(infile, outfile, section_size):
#    print("Preparing '%s' from '%s'"%(outfile, infile))

    # texture vectors
    texture_vectors = list()

    # calculate sections
    offset=0
    file_size = os.stat(infile).st_size
    file_modtime = int(os.path.getmtime(infile))
    md5 = hashlib.md5(open(infile, "rb").read()).hexdigest().upper()
    mod_size = section_size * 1000
    with open (infile, mode='rb') as f:
        while True:
            if offset % mod_size == 0:
                print("Processing %d of %d..."%(offset, file_size))
            b=f.read(section_size)
            if not b:
                break
            d=np.frombuffer(b,dtype='uint8') # binary array to numpy data
            texture_vectors.append(_texture_vector(d, section_size))
            offset += len(b)

    # save texture vector file
    json_tv = dict()
    json_tv["version"]=VERSION
    json_tv["filename"]=infile
    json_tv["file_group"]=os.path.basename(os.path.dirname(infile))
    json_tv["file_size"]=file_size
    json_tv["file_modtime"]=file_modtime
    json_tv["md5"]=md5
    json_tv["section_size"]=section_size
    json_tv["texture_names"] = texture_names
    json_tv["texture_vectors"] = texture_vectors
    with open(outfile, "w") as f:
        json.dump(json_tv, f, indent=4)

if __name__=="__main__":
    parser = ArgumentParser(prog='calc_tv.py',
                            description="Calculate texture vectors for a file.")
    parser.add_argument("filename", type=str, help="The input file.")
    parser.add_argument("-o", "--output_filename", type=str,
                 help="An alternate output filename, default is <filename>.tv.")
    parser.add_argument("-s", "--section_size", type=int, default=500,
                 help="The section size of the texture sample, default 500.")
    args = parser.parse_args()

    section_size = args.section_size
    if section_size < 1:
        print("Invalid section size %s"%section_size)
        sys.exit(1)
    infile = args.filename
    if not os.path.isfile(infile):
        print("Error: Input file '%s' does not exist."%infile)
        sys.exit(1)
    if args.output_filename:
        outfile = args.output_filename
    else:
        outfile = "%s.tv"%infile
    if os.path.exists(outfile):
        print("Error: Output file '%s' already exists."%outfile)
        sys.exit(1)

    print("Preparing '%s' from '%s'"%(outfile, infile))
    calc_tv(infile, outfile, section_size)
    print("Done.")

