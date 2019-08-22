from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QRadialGradient, QPen
from PyQt5.QtWidgets import QStyleOptionViewItem

"""Export graph picture.
"""

# export TV graph as image file.
def export_tv_graph(graph_filename, scene):

    # define the bounding rectangle for pixmap for painter to paint in
    w = int(scene.width()) + 40
    h = int(scene.height()) + 40
    pixmap = QPixmap(w, h)
    painter = QPainter(pixmap)
    painter.fillRect(0,0,w,h, QColor("#f0f0f0"))

    # get a default option object.  It is neither a QStyleOptionViewItem
    # nor a QStyleOptionGraphicsItem and we don't use it, but we need something.
    option = QStyleOptionViewItem()

    # paint the annotation, texture graphs, and similarity lines
    painter.translate(20,12)
    scene.tv_g_annotation.paint(painter, option, None)
    painter.translate(0,scene.tv_g_annotation.boundingRect().height()+35)
    scene.tv_g_texture1.paint(painter, option, None)
    painter.translate(0,100)
    scene.tv_g_lines.paint(painter, option, None)
    painter.translate(0,200)
    scene.tv_g_texture2.paint(painter, option, None)
    painter.translate(0,140)
    scene.tv_g_histogram.paint(painter, option, None)
    painter.end()

    # export
    try:
        pixmap.save(graph_filename)

    except Exception as e:
        status = "Error exporting TV graph image file '%s': %s" % (
                                         graph_filename, str(e))

