#from os.path import join, expanduser
from os.path import join

# path to the .tv files named by MD5
#_tv_dir = join(expanduser("~"), "exe/tv_files")
_tv_dir = "sbatch_tv_500"

# path to .tv file given MD5
def browser_tv_filename(md5):
    return join(_tv_dir, "%s.tv"%md5)

