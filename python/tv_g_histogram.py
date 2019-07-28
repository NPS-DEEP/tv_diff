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
from math import ceil

# Histogram Graph
"""Paint the annotated TV histogram inside the graph area."""
class TVGHistogram(QGraphicsItem):
    Type = QGraphicsItem.UserType + 4

    def __init__(self):
        super(TVGHistogram, self).__init__()

        # histogram height
        self.h = 200

        # histogram width
        self.w = 0

        # data
        self.similarity_data = None
        self.similarity_max = 0
        self.file_size1 = 0
        self.file_size2 = 0

    # call this if data changes
    def set_data(self, tv_data1, tv_data2, similarity_data):

        self.similarity_data = similarity_data
        self.similarity_max = similarity_data["max"]

        if tv_data1 and tv_data2:

            # values are defined
            self.file_size1 = tv_data1["file_size"]
            self.file_size2 = tv_data2["file_size"]

        else:
            self.file_size1 = 0
            self.file_size2 = 0

        # total graph width is num_buckets
        self.w = len(self.similarity_data["similarity_histogram"])

        self.prepareGeometryChange()

    def type(self):
        return TVGHistogram.Type

    # draw inside this rectangle
    def boundingRect(self):
        return QRectF(0, 0, self.w + 100, self.h+40)

    def paint(self, painter, option, widget):
        # no action
        if self.file_size1 + self.file_size2 == 0:
            return

        # set plot origin within graph
        painter.save()
        painter.translate(5+4, 5)

        # bounding box
        painter.drawRect(-1, -1, self.w+2, self.h+2)

        # histogram vertical scale
        h=self.h
        max_h = ceil(self.similarity_max * 1.05 / 10) * 10 # round ones digit
        if max_h < 100:
            max_h = 100
        scale = max_h/h

        # histograms
        histogram = self.similarity_data["similarity_histogram"]
        mean_power_histogram = self.similarity_data["mean_power_histogram"]
        compensated_histogram = self.similarity_data["compensated_histogram"]

        # similarity histogram
        painter.setPen(QColor(0,0,0,255)) # solid black
        for x in range(len(histogram)):
            y=round(histogram[x]/scale)
            painter.drawLine(x,h,x,max(h-y,0))

        # mean power histogram
        painter.setPen(QColor(0,0,255,64)) # blue opaque
        for x in range(len(mean_power_histogram)):
            y=round(mean_power_histogram[x]/scale)
            painter.drawLine(x,h,x,max(h-y,0))
        painter.setPen(QColor(0,0,0,255)) # solid black

        # compensated histogram
        painter.setPen(QColor(255,0,0,64)) # red opaque
        for x in range(len(compensated_histogram)):
            y=round(compensated_histogram[x]/scale)
            painter.drawLine(x,h,x,max(h-y,0))
        painter.setPen(QColor(0,0,0,255)) # solid black

        # x axis annotation
        w = self.w
        size1 = self.file_size1
        size2 = self.file_size2
        for i in (0, size1, size1+size2):
            x = round(i*w/(size1+size2))
            painter.drawLine(x, h+4, x, h+10)
            painter.drawText(x-4, h+18+10, "%s"%(i-size1))

        # y axis annotation
        painter.drawLine(w+4, h, w+8, h)
        painter.drawText(w+2+14, h+4, "0")
        painter.drawLine(w+4, 0, w+8, 0)
        painter.drawText(w+2+14, 4, "%s"%(round(h*scale)))

        painter.restore()

