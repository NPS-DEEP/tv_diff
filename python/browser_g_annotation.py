from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
                         QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtGui import QTransform
from PyQt5.QtGui import QPolygonF
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsView, QStyle)
from PyQt5.QtWidgets import QGraphicsSceneContextMenuEvent
from version_file import VERSION

# Similarity Lines
class BrowserGAnnotation(QGraphicsItem):
    Type = QGraphicsItem.UserType + 4

    def __init__(self):
        super(BrowserGAnnotation, self).__init__()

        # data
        self.annotation = "Click Node to open a .tv file."
        self._prepare()

    def describe_inputs(self, in_group, max_sd_similarity, max_ratio_similarity,
                                                              node1_index):
        if in_group:
            in_group_text = "Stay in group, "
        else:
            in_group_text = "All groups, "
        self.inputs_text="Similarity to node %d: %s" \
                         "Standard Deviation similarity > %.3f, " \
                         "Max/Sum similarity > %.6f"%(
                         node1_index, in_group_text,
                         max_sd_similarity, max_ratio_similarity)

    def describe_node(self, node_record):
        self.annotation = "%s\n\n%s"%(self.inputs_text, node_record.text())
        self._prepare()

    def describe_edge(self, edge_record, node_record_a, node_record_b):

        # make ordering reflect order in edge
        if edge_record.index1 == node_record_b.index:
            node_record_a,node_record_b = node_record_b,node_record_a

        self.annotation = "%s\n\n%s\n\n%s\n\n%s"%(self.inputs_text,
                                                  edge_record.text(),
                                                  node_record_a.text(),
                                                  node_record_b.text())
        self._prepare()

    # calculate texts and width
    def _prepare(self):

        # width and height
        lines=self.annotation.split("\n")
        w=500
        fm = QFontMetrics(QFont())
        for line in lines:
            w = max(w,fm.width(line))
        self.w = w
        self.h = 9 * 18

        self.prepareGeometryChange()

    def type(self):
        return BrowserGAnnotation.Type

    # draw inside this rectangle
    def boundingRect(self):
        return QRectF(0, 0, self.w+7, 20+self.h)

    def paint(self, painter, option, widget):
        painter.save()
        painter.translate(5, 20)
        painter.setPen(QPen(Qt.black, 0))
        painter.drawText(self.boundingRect(), self.annotation)
        painter.restore()

