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
#from graphics_rect import graphics_rect
from tv_scale_manager import original_scale

# TV Similarity Lines
class TVGLines(QGraphicsItem):
    Type = QGraphicsItem.UserType + 2

    def __init__(self):
        super(TVGLines, self).__init__()

        # height
        self.h = 200

        # bar width - must match texture_graph
        self.bar_width = 2.0

        # data
        self.tv_data1 = dict()
        self.tv_data2 = dict()
        self.step = 1

        # data width
        self.w = 0

        # scale
        self.scale = original_scale

        # draw fast sketch
        self.draw_sketch = False # must match default in draw_sketch checkbox

    def _prepare(self):

        # width
        # if both are defined then use wider of the two
        if self.tv_data1 and self.tv_data2:
            w1 = len(self.tv_data1["texture_vectors"]) * self.scale
            w2 = len(self.tv_data2["texture_vectors"]) * self.scale
            if w1 > w2:
                self.w = w1
            else:
                self.w = w2
        else:
            self.w = 0

        self.prepareGeometryChange()

    # call this if data or settings change
    def set_data(self, tv_data1, tv_data2, step, similarity_lines):
        self.tv_data1 = tv_data1
        self.tv_data2 = tv_data2
        self.step = step
        self.similarity_lines = similarity_lines
        self._prepare()

    # call this if scale changes
    def set_scale(self, scale):
        self.scale = scale
        self._prepare()

    def type(self):
        return TVGLines.Type

    # draw inside this rectangle
    def boundingRect(self):
        adjust = 2
        return QRectF(0 - adjust, 0 - adjust, self.w + adjust, self.h + adjust)

    def _draw_line(self, painter, bar_width, i, j):
        x1=i*bar_width
        y1=0
        x2=j*bar_width
        y2=200
        painter.drawLine(x1,y1,x2,y2)

    def paint(self, painter, option, widget):
        if not self.tv_data1 or not self.tv_data2:
            return

        painter.save()
        painter.translate(5+4, 20) # same as texture_graph

        bar_width = self.scale
        similarity_lines = self.similarity_lines
        step = self.step

        # paint similarity lines from left to right
        for i, values in similarity_lines.items():
            for j in values:
                 self._draw_line(painter, bar_width, i,j)

        painter.restore()

