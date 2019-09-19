from collections import defaultdict
from show_popup import show_popup
import csv
from tv_time import t_string
from browser_data_paths import GRAPH_NODES, GRAPH_EDGES
#from PyQt5.QtCore import QObject # for signal/slot support
#from PyQt5.QtCore import pyqtSignal # for signal/slot support
#from PyQt5.QtCore import pyqtSlot # for signal/slot support

#from settings_manager import settings
#from settings_store import texture_compatible
#from similarity_math import generate_similarity_data, empty_similarity_data

"""Provides graph data:

  nodes = list<NodeRecord> where node[0] is Node 1.
  edges = dict<(n1,n2):<EdgeRecord> where n1<n2
  connections = dict<n:set<adjacent n's> >

"""

# throws ValueError
# ['Id', 'Name', 'Group', 'Size', 'Modtime', 'MD5']
class NodeRecord():
    def __init__(self, row):
        self.index=int(row[0])
        self.filename = row[1]
        self.file_group = row[2]
        self.file_size = int(row[3])
        self.modtime = int(row[4])
        self.file_md5 = row[5]

    def debug_text(self):
        text="node %d: group %s"%(self.index, self.file_group)
        return text

    def text(self):
        return "Node %d: %s\n" \
               "Group: '%s', Size: %d, Modtime: %s, MD5: %s"%(
               self.index, self.filename,
               self.file_group, self.file_size, t_string(self.modtime),
               self.file_md5)

# throws ValueError
['Source', 'Target', 'SD', 'Mean', 'Max', 'Sum']
class EdgeRecord():
    def __init__(self, row):
        self.index1=int(row[0])
        self.index2=int(row[1])
        self.sd = float(row[2])
        self.mean = float(row[3])
        self.maxv = int(row[4])
        self.sumv = int(row[5])

    def debug_text(self):
        text="edge %d - %d: "%(self.index1, self.index2, self.sd)
        return text

    def text(self):
        text = "Edge %d - %d: " \
               "Standard deviation: %.4f, Mean: %.4f, Max: %d, Sum: %d, " \
               "Max/Sum: %.4f"%(
               self.index1, self.index2,
               self.sd, self.mean, self.maxv, self.sumv, self.maxv/self.sumv)
        return text

def read_nodes():
    nodes = list()
    print("Reading nodes from '%s'..."%GRAPH_NODES)
    with open(GRAPH_NODES) as f:
        reader = csv.reader(f)
        for row in reader:
            try:
                node = NodeRecord(row)
                if node.index != len(nodes) + 1:
                    raise Exception("Bad: %d, %d"%(node.index, len(nodes)))
                nodes.append(node)
            except ValueError as e:
                print("Node comment:")
                print(row)
    print("Done reading nodes")
    return nodes

def read_edges():
    edges = dict()
    connections = defaultdict(set)
#    return edges,connections # zzfast
    print("Reading edges from '%s'..."%GRAPH_EDGES)
    with open(GRAPH_EDGES) as f:
       reader = csv.reader(f)
       for row in reader:
           try:
               edge = EdgeRecord(row)
               index1 = edge.index1
               index2 = edge.index2
               if index1 < index2:
                   edges[(index1, index2)] = edge
               else:
                   edges[(index2, index1)] = edge

               connections[index1].add(index2)
               connections[index2].add(index1)
           except ValueError as e:
               print("Edge comment:")
               print(row)
    print("Done reading edges")
    return edges, connections

