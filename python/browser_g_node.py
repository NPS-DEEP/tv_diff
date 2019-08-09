# Adapted from https://raw.githubusercontent.com/baoboa/pyqt5/master/examples/graphicsview/elasticnodes.py

from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtCore import pyqtSlot
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
from browser_graph_constants import T_MIN, T_SCALE, Y_MAX

# QGraphicsItem Node
class BrowserGNode(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, node_record, is_node1, similarity, change_manager):
        super(BrowserGNode, self).__init__()

        # attributes
        self.node_record = node_record
        self.is_node1 = is_node1
        self.similarity = similarity
        self.change_manager = change_manager

        # graphicsItem mode
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(1) # stacking order when drawing

        # path region for mouse detection
        self.mouse_path = QPainterPath()
        self.mouse_path.addEllipse(-10, -10, 20, 20)

    # set node position
    def set_position(self, dy, scale, max_similarity):
        x = (self.node_record.modtime-T_MIN)/T_SCALE * scale
        if self.is_node1:
            y = dy + 0
        else:
            y = dy + Y_MAX * (1 - self.similarity/max_similarity) * scale
        self.setPos(QPointF(x,y))

        self.prepareGeometryChange()

    def type(self):
        return BrowserGNode.Type

    # draw inside this rectangle
    def boundingRect(self):
        adjust = 2.0
        return QRectF(-10 - adjust, -10 - adjust, 20 + adjust, 20 + adjust)

    # mouse hovers when inside this rectangle
    def shape(self):
        return self.mouse_path

    def paint(self, painter, option, widget):

        if self.is_node1:
            color=Qt.green
            dark_color=Qt.darkGreen
        else:
            color=Qt.yellow
            dark_color=Qt.darkYellow

        gradient = QRadialGradient(-3, -3, 10)
        if option.state&QStyle.State_MouseOver:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(color).lighter(120))
            gradient.setColorAt(0, QColor(dark_color).lighter(120))
        else:
            gradient.setColorAt(0, color)
            gradient.setColorAt(1, dark_color)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

        # node text
        painter.setPen(QPen(QColor(Qt.black), 0))
        painter.drawText(13, 4, "%s"%self.node_record.index)

    def hoverEnterEvent(self, event):
        self.change_manager.signal_node_hovered.emit(self.node_record)
        super(BrowserGNode, self).hoverEnterEvent(event)

    def mousePressEvent(self, event):
        super(BrowserGNode, self).mousePressEvent(event)
        if not self.is_node1:
            # select this node as file1
            self.change_manager.change_node_record1(self.node_record)

