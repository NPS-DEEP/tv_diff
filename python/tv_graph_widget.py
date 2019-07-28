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
from tv_g_annotation import TVGAnnotation
from tv_g_texture import TVGTexture
from tv_g_lines import TVGLines
from tv_g_histogram import TVGHistogram

"""TVGraphWidget provides the main QGraphicsView.  It manages signals
and wraps these:
  * TVGraphView
  * TVGraphScene
"""

# GraphicsView
class TVGraphView(QGraphicsView):
    def __init__(self):
        super(TVGraphView, self).__init__()

        self.viewport_cursor = Qt.ArrowCursor
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        self.setMinimumSize(300, 300)


class TVGraphScene(QGraphicsScene):

    def __init__(self):
        super(TVGraphScene, self).__init__()
        y=0

        # general annotation
        self.tv_g_annotation = TVGAnnotation()
        self.addItem(self.tv_g_annotation)
        self.tv_g_annotation.setPos(QPointF(0,100-18*(6+1))) # height depends
        y+= 18*(6+1)

        # texture graph 1
        self.tv_g_texture1 = TVGTexture()
        self.addItem(self.tv_g_texture1)
        self.tv_g_texture1.setPos(QPointF(0,y))
        y+= 100

        # similarity lines
        self.tv_g_lines = TVGLines()
        self.addItem(self.tv_g_lines)
        self.tv_g_lines.setPos(QPointF(0,y))
        y+= 200

        # texture graph 2
        self.tv_g_texture2 = TVGTexture()
        self.addItem(self.tv_g_texture2)
        self.tv_g_texture2.setPos(QPointF(0,y))
        y+= 140

        # histogram graph
        self.tv_g_histogram = TVGHistogram()
        self.addItem(self.tv_g_histogram)
        self.tv_g_histogram.setPos(QPointF(0,y))

# TVGraphWidget
class TVGraphWidget(QObject):

    def __init__(self, signal_data_loaded, signal_tv_scale_changed):
        super(TVGraphWidget, self).__init__()

        # TVGraphWidget's scene and view objects
        self.scene = TVGraphScene()
        self.view = TVGraphView()
        self.view.setScene(self.scene)

        # connect to schedule repaint on change
        signal_data_loaded.connect(self.change_data)
        signal_tv_scale_changed.connect(self.change_scale)

    # call this to accept data change
    @pyqtSlot(dict, dict, int, dict)
    def change_data(self, tv_data1, tv_data2, step, similarity_data):
        self.scene.tv_g_annotation.set_data(tv_data1, tv_data2, step,
                                       similarity_data)
        self.scene.tv_g_texture1.set_data(tv_data1, step)
        self.scene.tv_g_texture2.set_data(tv_data2, step)
        self.scene.tv_g_lines.set_data(tv_data1, tv_data2, step,
                                       similarity_data["similarity_lines"])
        self.scene.tv_g_histogram.set_data(tv_data1, tv_data2,
                                       similarity_data)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

    # call this to accept scale change
    @pyqtSlot(float)
    def change_scale(self, scale):
        self.scene.tv_g_annotation.set_scale(scale)
        self.scene.tv_g_texture1.set_scale(scale)
        self.scene.tv_g_texture2.set_scale(scale)
        self.scene.tv_g_lines.set_scale(scale)
        self.scene.setSceneRect(self.scene.itemsBoundingRect())

