# Adapted from https://raw.githubusercontent.com/baoboa/pyqt5/master/examples/graphicsview/elasticnodes.py

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
from tv_scale_manager import original_scale

# Texture Graph
class TVGTexture(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self):
        super(TVGTexture, self).__init__()

        # height
        self.h = 100

        # data
        self.tv_data = dict()
        self.step = 1

        # data width
        self.w = 0

        # scale
        self.scale = original_scale

        # color matrix
        self.colors = list()
        for i in range(256):
            self.colors.append(QColor(i,i,i))

    def _prepare(self):

        # total graph width
        if self.tv_data:
            self.w = len(self.tv_data["texture_vectors"]) * self.scale
            self.section_size = self.tv_data["section_size"]
        else:
            self.w = 0
            self.section_size = 0

        self.prepareGeometryChange()

    # call this if data changes
    def set_data(self, tv_data, step):
        self.tv_data = tv_data
        self.step = step
        self._prepare()

    # call this if scale changes
    def set_scale(self, scale):
        self.scale = scale
        self._prepare()

    def type(self):
        return TVGTexture.Type

    # draw inside this rectangle
    def boundingRect(self):
        return QRectF(0, 0, self.w+15, self.h+40)

    def paint(self, painter, option, widget):
        if not self.tv_data:
            return

        painter.save()
        painter.translate(5+4, 20)

        bar_width = self.scale
        data = self.tv_data["texture_vectors"]
        num_elements = len(self.tv_data["texture_names"])
        element_height = self.h / num_elements
        step = self.step

        # paint texture vector items from left to right
        for i in range(0, len(data), step): # data length
            for j in range(num_elements):
                painter.setPen(self.colors[data[i][j]])
                x=i*bar_width
                y=j*element_height
                painter.drawLine(x, y, x, y+element_height)

        # paint annotation
        painter.setPen(QPen(Qt.black, 0))
        tick_step = round(100 / bar_width)
        if tick_step < 10:
            tick_step = 10
        y=0
        section_size = self.section_size
        for i in range(0, len(data), tick_step):
            x=i*bar_width
            painter.drawLine(x,y-2,x,y-8)
            painter.drawText(x-4, y-10, "%s"%(i*section_size))

        painter.restore()

