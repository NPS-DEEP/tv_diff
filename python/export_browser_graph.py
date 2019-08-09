from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QColor, QLinearGradient, QBrush, QRadialGradient, QPen
from PyQt5.QtGui import QTextOption
from PyQt5.QtWidgets import QStyleOptionViewItem
from version_file import VERSION

"""Export browser graph picture.
"""

# export browser graph as image file.
def export_browser_graph(graph_filename, scene):

    # define the bounding rectangle for pixmap for painter to paint in
    w = int(scene.width()) + 40
    if w < 840:
        # adjust for when zoomed small
        w=840
    h = int(scene.height()) + 40 + 200
    pixmap = QPixmap(w, h)
    painter = QPainter(pixmap)
    painter.fillRect(0,0,w,h, QColor("#f0f0f0"))

    # get a default option object.  It is neither a QStyleOptionViewItem
    # nor a QStyleOptionGraphicsItem and we don't use it, but we need something.
    option = QStyleOptionViewItem()

    # paint the annotation
    painter.translate(20,20)
    scene.g_annotation.paint(painter, option, None)

    # paint the graph
    painter.translate(40,200)

    # nodes, edges, and axis
    for edge in scene.g_edges:
        edge.paint(painter, option, None)
    for node in scene.g_nodes:
        painter.save()
        painter.translate(node.pos())
        node.paint(painter, option, None)
        painter.restore()
    scene.g_axis.paint(painter, option, None)
    painter.end()

    # export
    try:
        pixmap.save(graph_filename)

    except Exception as e:
        status = "Error exporting browser graph image file '%s': %s" % (
                                         graph_filename, str(e))

