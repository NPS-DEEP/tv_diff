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
from PyQt5.QtWidgets import QTextEdit
from browser_graph_data_reader import NodeRecord, EdgeRecord

class BrowserAnnotationWidget(QObject):

    def __init__(self, change_manager):
        super(BrowserAnnotationWidget, self).__init__()

        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.setPlainText("Open a .tv file.")
        self.text_box.setMinimumSize(900, 190)

        change_manager.signal_inputs_changed.connect(self.describe_node)
        change_manager.signal_node_hovered.connect(self.describe_node)
        change_manager.signal_edge_hovered.connect(self.describe_edge)

    # call this to set node text
    @pyqtSlot(NodeRecord)
    def describe_node(self, node_record):
        self.text_box.setPlainText(node_record.text())

    # call this to set edge, node_a, and node_b text
    @pyqtSlot(EdgeRecord, NodeRecord, NodeRecord)
    def describe_edge(self, edge_record, node_record_a, node_record_b):

        # make ordering reflect order in edge
        if edge_record.index1 == node_record_b.index:
            node_record_a,node_record_b = node_record_b,node_record_a

        self.text_box.setPlainText("%s\n\n%s\n\n%s"%(
                                   edge_record.text(),
                                   node_record_a.text(),
                                   node_record_b.text()))

