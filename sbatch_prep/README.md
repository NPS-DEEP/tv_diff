This directory contains data and the program for preparing
the dataset used by the `tv_browser.py` tool.

File `set_modtimes.py` along with `exe_modtimes.out` and
`out_timestamps.out` sets file file
modification times based on modification times from extracted data.
The time selected is the latest reasonable time for the file
based on its MD5 value.

File `md5_copy.py` copys generated `.tv` files for use by `tv_browser.py`,
renaming them to the MD5 values of the files they were generated from.
