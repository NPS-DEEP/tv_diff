# Adapted from https://raw.githubusercontent.com/baoboa/pyqt5/master/examples/graphicsview/elasticnodes.py

from math import sin, cos, tan, atan2, pi
from PyQt5.QtCore import (QLineF, QPointF, QRectF, QSizeF)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter,
                         QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtGui import QTransform
from PyQt5.QtGui import QPolygonF
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QPainterPath
from PyQt5.QtGui import QPainterPathStroker
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsView, QStyle)
from PyQt5.QtWidgets import QGraphicsSimpleTextItem
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QGraphicsSceneContextMenuEvent

# Edge

class BrowserGEdge(QGraphicsItem):
    Type = QGraphicsItem.UserType + 2

    def __init__(self, edge_record, g_node_a, g_node_b, change_manager):
        super(BrowserGEdge, self).__init__()

        # attributes
        self.edge_record = edge_record
        self.g_node_a = g_node_a
        self.g_node_b = g_node_b
        self.change_manager = change_manager

        # graphicsItem mode
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

    def set_position(self):
        self.p1 = self.mapFromItem(self.g_node_a, 0, 0)
        self.p2 = self.mapFromItem(self.g_node_b, 0, 0)

        # the path region for mouse detection
        self.edge_path = QPainterPath(self.p1)
        self.edge_path.lineTo(self.p2)

        self.prepareGeometryChange()

    def type(self):
        return BrowserGEdge.Type

    def boundingRect(self):
        extra = 10
        return self.edge_path.boundingRect().adjusted(-extra, -extra,
                                                            extra, extra)

    def shape(self):
        # note: path without stroker includes concave shape, not just edge path
        return self.edge_path

    def paint(self, painter, option, widget):

        # paint edge shape of path without brush fill
        line_width = 2
        if option.state & QStyle.State_MouseOver:
            line_color = Qt.red
        else:
            line_color = Qt.blue
        painter.strokePath(self.edge_path, QPen(line_color, line_width,
                                   Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

    def hoverEnterEvent(self, event):
        self.change_manager.signal_edge_hovered.emit(self.edge_record,
                                                     self.g_node_a.node_record,
                                                     self.g_node_b.node_record)
        super(BrowserGEdge, self).hoverEnterEvent(event)

    def mousePressEvent(self, event):
        self.change_manager.edge_selected_event(self.edge_record,
                                                self.g_node_a.node_record,
                                                self.g_node_b.node_record)
        super(BrowserGEdge, self).mousePressEvent(event)

