#from os.path import join, expanduser
from os.path import join

GRAPH_NODES="../data/sbatch_graph_500/nodes.csv"
GRAPH_EDGES="../data/sbatch_graph_500/edges.csv"
_TV_DIR="../data/sbatch_tv_500/"

# path to .tv file given MD5
def browser_tv_filename(md5):
    return join(_TV_DIR, "%s.tv"%md5)

