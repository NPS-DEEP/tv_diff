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
from settings_manager import settings
from settings_store import texture_compatible
from tv_time import t_string

def _file_metadata(filenum, tv_data):
    # file metadata
    text = ("File %d: %s\nSize: %d Modtime: %s MD5: %s"%(
            filenum,
            tv_data["filename"],
            tv_data["file_size"],
            t_string(tv_data["file_modtime"]),
            tv_data["md5"]))
    return text

# Similarity Lines
class TVGAnnotation(QGraphicsItem):
    Type = QGraphicsItem.UserType + 3

    def __init__(self):
        super(TVGAnnotation, self).__init__()

        # data
        self.tv_data1 = dict()
        self.tv_data2 = dict()
        self.scale = "1:1"
        self.step = 1

        self._prepare()

    def _texture_thresholds(self):

        # make sure the texture names match
        if self.tv_data1 and not texture_compatible(settings["names"],
                                     self.tv_data1["texture_names"]):
            return "Texture fields do not match"
        if self.tv_data2 and not texture_compatible(settings["names"],
                                     self.tv_data2["texture_names"]):
            return "Texture fields do not match"

        # return texture
        text = "Acceptance thresholds:"
        for i in range(len(settings["names"])):
            if settings["use"][i]:
                text += "  %s: %d"%(settings["names"][i],
                                    settings["threshold"][i])
            else:
                text += "  %s: not used"%settings["names"][i]
        return text

    # calculate texts and width
    def _prepare(self):

        # program settings: version, scale, step, section size
        if self.tv_data1 or self.tv_data2:
            if self.tv_data1:
                section_size = self.tv_data1["section_size"]
            else:
                section_size = self.tv_data2["section_size"]
            text1 = "Texture Vector Similarity Version %s  " \
                    "Scale: %s  Step: %s  Section size: %d"%(
                    VERSION, self.scale, self.step, section_size)
        else:
            text1 = ""

        # thresholds and number of buckets
        if self.tv_data1 and self.tv_data2:
            text2 = self._texture_thresholds()
            text2 = "%s  Buckets: %d"%(text2,
                    len(self.similarity_data["similarity_histogram"]))
        else:
            text2 = ""

        # similarity
        if self.tv_data1 and self.tv_data2:
            d=self.similarity_data
            text3 = "Compensated statistics: " \
                    "SD: %.4f, Mean: %.4f, Max: %d, Sum: %d, Max/Sum: %.4f"%(
               d["sd"], d["mean"], d["max"], d["sum"], d["max"]/d["sum"])
        else:
            text3 = ""

        # file1
        if self.tv_data1:
            text4 = _file_metadata(1, self.tv_data1)
        else:
            text4 = ""

        # file2
        if self.tv_data2:
            text5 = _file_metadata(2, self.tv_data2)
        else:
            text5 = ""

        # total
        self.annotation = "%s\n%s\n%s\n%s\n%s"%(
                                          text1,text2,text3,text4,text5)

        # width and height
        lines=self.annotation.split("\n")
        w=500
        fm = QFontMetrics(QFont())
        for line in lines:
            w = max(w,fm.width(line))
        self.w = w
        self.h = (len(lines)+1) * 12

        self.prepareGeometryChange()

    # call this if data or settings change
    def set_data(self, tv_data1, tv_data2, step, similarity_data):

        self.tv_data1 = tv_data1
        self.tv_data2 = tv_data2
        self.step = step
        self.similarity_data = similarity_data

        self._prepare()

    # call this if scale changes
    def set_scale(self, scale):
        if scale < 1:
            self.scale = "1:%d"%round(1/scale)
        else:
            self.scale = "%d:1"%round(scale)
     
        self._prepare()

    def type(self):
        return TVGAnnotation.Type

    # draw inside this rectangle
    def boundingRect(self):
        return QRectF(0, 0, self.w+7, self.h+12)

    def paint(self, painter, option, widget):

        painter.save()
        painter.translate(5, 12)
        painter.setPen(QPen(Qt.black, 0))
        painter.drawText(self.boundingRect(), self.annotation)
        painter.restore()

