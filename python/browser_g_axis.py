from math import sin, cos, tan, atan2, pi
from PyQt5.QtCore import (QLineF, QPointF, QRectF, QSizeF)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
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
from browser_change_manager import browser_original_scale
from browser_graph_constants import X_MAX, Y_MAX

# Axis

class BrowserGAxis(QGraphicsItem):
    Type = QGraphicsItem.UserType + 3

    # x tick position given year
    def _x(self, year, t_scale):
        x=(year-1995)/(2020-1995) * t_scale
        return x

    def __init__(self, y_label):
        super(BrowserGAxis, self).__init__()
        self.y_label = y_label
        self.scale = 1
        self.max_similarity = 0

    def set_position(self, dy, scale, max_similarity, node1_index):
        self.scale = scale
        self.max_similarity = max_similarity
        self.node1_index = node1_index
        self.setPos(0,dy)

        self.bounding_rect = QRectF(-80,-10,
                                    X_MAX*scale+80+40, Y_MAX*scale+10+45)

        self.prepareGeometryChange()

    def type(self):
        return BrowserGAxis.Type

    def boundingRect(self):
        return self.bounding_rect

    def paint(self, painter, option, widget):

        gap = 5
        tick = 8
        y_max = Y_MAX * self.scale
        x_max = X_MAX * self.scale
        max_similarity = self.max_similarity

        # axis
        painter.drawLine(0, y_max, x_max, y_max)
        painter.drawLine(0, y_max, 0, 0)

        # x axis annotation
        for year in range(1995, 2021, 5):
            x=self._x(year, x_max)

            painter.drawLine(x,y_max+gap, x,y_max+gap+tick)
            painter.drawText(x-15,y_max+gap+tick+18, "%d"%year)

        painter.drawText(x_max/2-15, y_max+gap+tick+30, "Year")

        # y axis annotation
        painter.drawLine(-gap, y_max, -gap-tick, y_max)
        if max_similarity > 0:
            painter.drawText(-gap-tick-38, 0+4, "%.2f"%max_similarity)

        painter.drawLine(-gap,0, -gap-tick,0)
        painter.drawText(-gap-tick-14, y_max+4, "0")

        painter.save()
        painter.translate(-32, y_max/2)
        painter.rotate(-90)
        y_label="Edge %s\nwith respect to Node %d"%(
                                          self.y_label, self.node1_index)
        painter.drawText(self.boundingRect(), y_label)
        painter.restore()

