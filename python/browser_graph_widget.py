from PyQt5.QtCore import (QLineF, QPointF, qrand, QRect, QRectF, QSizeF, Qt)
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QObject
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
                         QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsView, QStyle)
from PyQt5.QtWidgets import QGraphicsScene
import itertools
from browser_graph_data_reader import NodeRecord
from browser_change_manager import browser_original_scale
from browser_g_node import BrowserGNode
from browser_g_edge import BrowserGEdge
from browser_g_axis import BrowserGAxis
from browser_g_annotation import BrowserGAnnotation
from browser_graph_data_reader import NodeRecord, EdgeRecord


"""BrowserGraphWidget provides the main QGraphicsView.  It manages signals
and wraps these:
  * BrowserGraphView
  * BrowserGraphScene

max_sd_similarity is the largest SD similarity value in the dataset
max_ratio_similarity is the largest Max/Sum similarity value in the dataset
"""

# GraphicsView
class BrowserGraphView(QGraphicsView):
    def __init__(self):
        super(BrowserGraphView, self).__init__()

        self.viewport_cursor = Qt.ArrowCursor
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setMinimumSize(300, 300)


class BrowserGraphScene(QGraphicsScene):

    def __init__(self):
        super(BrowserGraphScene, self).__init__()
        self.scale = browser_original_scale
        self.g_nodes = list()
        self.g_edges = list()
        self.max_sd_similarity = 1
        self.max_ratio_similarity = 0.000001 #zzz

        # annotation
        self.g_annotation = BrowserGAnnotation()
        self.addItem(self.g_annotation)

    def set_scene(self, g_nodes, g_edges,
                  max_sd_similarity, max_ratio_similarity):

        self.g_nodes = g_nodes
        self.g_edges = g_edges
        self.max_sd_similarity = max_sd_similarity
        self.max_ratio_similarity = max_ratio_similarity

        # use Python to delete previous items instead of QGraphicsScene
        for item in self.items():
            self.removeItem(item)

        # add annotation
        self.addItem(self.g_annotation)

        # add graph node items
        for g_node in g_nodes:
            self.addItem(g_node)

        # add graph edge items
        for g_edge in g_edges:
            self.addItem(g_edge)

        # add axis
        self.g_axis = BrowserGAxis(max_sd_similarity)
        self.addItem(self.g_axis)

        # set scale
        self.set_scale(self.scale)

    def set_scale(self, scale):
        self.scale = scale
        for node in self.g_nodes:
            node.set_position(self.scale, self.max_sd_similarity)
        for edge in self.g_edges:
            edge.set_position()
        self.g_axis.set_scale(self.scale)

        # reset bounding rectangle
        self.setSceneRect(self.itemsBoundingRect())

class BrowserGraphWidget(QObject):

    def __init__(self, all_nodes, all_edges, all_connections, change_manager):
        super(BrowserGraphWidget, self).__init__()

        self.all_nodes = all_nodes
        self.all_edges = all_edges
        self.all_connections = all_connections
        self.change_manager = change_manager

        # BrowserGraphWidget's scene and view objects
        self.scene = BrowserGraphScene()
        self.view = BrowserGraphView()
        self.view.setScene(self.scene)

        # connect to schedule repaint on change
        change_manager.signal_inputs_changed.connect(self.change_inputs)

        # connect to schedule repaint on rescale
        change_manager.signal_browser_scale_changed.connect(self.change_scale)

        # connect to change annotation on node or edge hover
        change_manager.signal_node_hovered.connect(self.change_node_annotation)
        change_manager.signal_edge_hovered.connect(self.change_edge_annotation)

    def _make_g_nodes_g_edges(self, node_record1, in_group,
                              sd_threshold, max_over_sum_threshold):
        # We track node similarity then calculate node points.
        # Then we can create correctly located edge points.

        # nodes
        max_sd_similarity = 0.0
        max_ratio_similarity = 0.0
        g_nodes = list()

        # node 1
        g_node1 = BrowserGNode(node_record1, True, 0, self.change_manager)
        g_nodes.append(g_node1)

        # require file group membership
        if in_group:
            require_group = node_record1.file_group
        else:
            require_group = None

        # other nodes adjacent to node 1
        node1_index = node_record1.index
        for n in self.all_connections[node1_index]:
            node_record = self.all_nodes[n-1]

            # skip if using in_group and not a member
            if require_group and require_group != node_record.file_group:
                continue

            # get edge record
            if node1_index < n:
                edge_record = self.all_edges[(node1_index, n)]
            else:
                edge_record = self.all_edges[(n, node1_index)]

            # skip if below SD threshold
            if edge_record.sd < sd_threshold:
                continue

            # skip if below max/min threshold
            if edge_record.maxv/edge_record.sumv < max_over_sum_threshold:
                continue

            # accept node
            sd_similarity = edge_record.sd
            g_nodes.append(BrowserGNode(node_record, False,
                           sd_similarity, self.change_manager))
            max_sd_similarity = max(sd_similarity, max_sd_similarity)
            max_ratio_similarity = max(sd_similarity, max_ratio_similarity)

        # edges
        g_edges = list()
        for g_node_a, g_node_b in itertools.combinations(g_nodes, 2):

            # get edge record
            i_a = g_node_a.node_record.index
            i_b = g_node_b.node_record.index
            if i_a > i_b:
                # lookup requires i_a < i_b
                i_a, i_b = i_b, i_a

            if (i_a,i_b) in self.all_edges:
                edge_record = self.all_edges[(i_a, i_b)]

                # skip if below SD threshold
                if edge_record.sd < sd_threshold:
                    continue

                # skip if below max/min threshold
                if edge_record.maxv/edge_record.sumv < max_over_sum_threshold:
                    continue

                g_edges.append(BrowserGEdge(edge_record, g_node_a, g_node_b,
                                                  self.change_manager))

        return g_nodes, g_edges, max_sd_similarity, max_ratio_similarity

    # call this to accept input change
    @pyqtSlot(NodeRecord, bool, float, float)
    def change_inputs(self, node_record1, in_group,
                      sd_threshold, max_over_sum_threshold):
        g_nodes, g_edges, max_sd_similarity, max_ratio_similarity = \
                      self._make_g_nodes_g_edges(
                                         node_record1, in_group,
                                         sd_threshold, max_over_sum_threshold)
        self.scene.set_scene(g_nodes, g_edges,
                             max_sd_similarity, max_ratio_similarity)
        self.scene.g_annotation.describe_node(node_record1)

    # call this to accept browser scale change
    @pyqtSlot(float)
    def change_scale(self, scale):
        self.scene.set_scale(scale)

    @pyqtSlot(NodeRecord)
    def change_node_annotation(self, node_record):
        self.scene.g_annotation.describe_node(node_record)

    # call this to set edge, node_a, and node_b text
    @pyqtSlot(EdgeRecord, NodeRecord, NodeRecord)
    def change_edge_annotation(self, edge_record, node_record_a, node_record_b):
        self.scene.g_annotation.describe_edge(edge_record,
                                        node_record_a, node_record_b)

