from PyQt5.QtWidgets import QMainWindow, QAction, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
import os
import ntpath
from tv_icons import window_icon
from version_file import VERSION
from browser_change_manager import BrowserChangeManager
from browser_file_group_cb import BrowserFileGroupCB
from browser_threshold_sliders import BrowserThresholdSliders
#from browser_graph_main_widget import BrowserGraphMainWidget
from browser_graph_data_reader import read_nodes, read_edges
from browser_graph_widget import BrowserGraphWidget
from browser_file1_window import BrowserFile1Window
from browser_edge_window import BrowserEdgeWindow
from tv_main_window import TVMainWindow
from export_browser_graph import export_browser_graph

"""main window containing toolbar and central widget.
"""
class MasterQMainWindow(QMainWindow):
    def __init__(self, child_window):
        super(MasterQMainWindow, self).__init__()
        self.child_window = child_window

    # override closure
    def closeEvent(self, event):
        self.child_window.close()
        super(MasterQMainWindow, self).closeEvent(event)

class BrowserMainWindow(QObject):

    def __init__(self):
        super(BrowserMainWindow, self).__init__()

        # user's preferred JPG tv browser graph path
        self.preferred_browser_graph_dir = os.path.expanduser("~")

        # graph data
        self.all_nodes = read_nodes()
        self.all_edges, self.all_connections = read_edges()

        # change manager
        starting_node_record = self.all_nodes[0]
        self.browser_change_manager = BrowserChangeManager(
                                       starting_node_record, True, 1.0)

        # file group checkbox
        self.browser_file_group_cb = BrowserFileGroupCB(
                                       self.browser_change_manager)

        # browser threshold slider
        self.browser_threshold_sliders = BrowserThresholdSliders(
                                       self.browser_change_manager)

        # open file1 window
        self.browser_file1_window = BrowserFile1Window(self.all_nodes,
                                                 self.browser_change_manager)

        # open edge window
        self.browser_edge_window = BrowserEdgeWindow(self.all_nodes,
                                                 self.browser_change_manager)
        # tv window
        self.tv_main_window = TVMainWindow(
                            self.browser_change_manager.signal_want_tv_window)

        # master tv browser window
        self.w = MasterQMainWindow(self.tv_main_window.w)

        # main window decoration
        self.w.setGeometry(0,0,920,630)
        self.w.setWindowTitle("Texture Vector Browser Version %s"%VERSION)
        self.w.setWindowIcon(QIcon(window_icon))

        # the similarity graph main widget
        self.browser_graph_widget = BrowserGraphWidget(
                        self.all_nodes, self.all_edges, self.all_connections,
                        self.browser_change_manager)

        # the similarity graph
        self.w.setCentralWidget(self.browser_graph_widget.view)

        # actions
        self.define_actions()

        # toolbar
        self.add_toolbar()

    # actions
    def define_actions(self):
        # open file 1
        self.action_open_file1 = QAction(QIcon(
                       "icons/circle_green.png"), "&Node...", self)
        self.action_open_file1.setToolTip("Open .tv file node")
        self.action_open_file1.triggered.connect(self.select_and_open_file1)

        # open edge
        self.action_open_edge= QAction(QIcon(
                       "icons/list-remove-3.png"), "&Edge...", self)
        self.action_open_edge.setToolTip("View similarity edge")
        self.action_open_edge.triggered.connect(self.select_and_open_edge)

        # scale in
        self.action_scale_in = QAction(QIcon(
                       "icons/zoom-in-3.png"), "&+", self)
        self.action_scale_in.setToolTip("Scale in")
        self.action_scale_in.triggered.connect(
                                        self.browser_change_manager.scale_in)

        # scale out
        self.action_scale_out = QAction(QIcon(
                       "icons/zoom-out-3.png"), "&-", self)
        self.action_scale_out.setToolTip("Scale out")
        self.action_scale_out.triggered.connect(
                                        self.browser_change_manager.scale_out)

        # scale original size
        self.action_scale_original = QAction(QIcon(
                       "icons/zoom-original-2.png"), "&1", self)
        self.action_scale_original.setToolTip("Scale to original size")
        self.action_scale_original.triggered.connect(
                                  self.browser_change_manager.scale_original)

        # action export browser graph as image file
        self.action_export_browser_graph = QAction(QIcon(
                       "icons/document-export-4.png"),
                       "&Export...", self)
        self.action_export_browser_graph.setToolTip(
                                        "Export browser graph as image file")
        self.action_export_browser_graph.triggered.connect(
                                     self.select_and_export_browser_graph)

    # toolbar items
    def add_toolbar(self):
        toolbar = self.w.addToolBar("TV Browser Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(self.action_open_file1)
        toolbar.addAction(self.action_open_edge)
        toolbar.addWidget(self.browser_file_group_cb.browser_file_group_cb)
        toolbar.addWidget(QLabel(" ")) # before slider
        toolbar.addWidget(self.browser_threshold_sliders)
        toolbar.addWidget(QLabel("  ")) # after slider
        toolbar.addAction(self.action_scale_in)
        toolbar.addAction(self.action_scale_out)
        toolbar.addAction(self.action_scale_original)
        toolbar.addAction(self.action_export_browser_graph)

    ############################################################
    # action handlers
    ############################################################

    @pyqtSlot()
    def select_and_open_file1(self):
        self.browser_file1_window.show_window()

    @pyqtSlot()
    def select_and_open_edge(self):

        # get edge records from browser_graph_widget
        g_edges = self.browser_graph_widget.scene.g_sd_edges
        edge_records = list()
        for g_edge in g_edges:
            edge_records.append(g_edge.edge_record)
        self.browser_edge_window.show_window(edge_records)

    # export browser graph as image file
    @pyqtSlot()
    def select_and_export_browser_graph(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # suggested filename
        suggested_filename = "tv_browser_graph.png"

        filename, _ = QFileDialog.getSaveFileName(self.w,
        "Export browser graph image file",
        os.path.join(self.preferred_browser_graph_dir, suggested_filename),
        "TV graph image files (*.png);;All Files (*)", options=options)

        if filename:
            # remember the preferred path
            head, _tail = os.path.split(filename)
            self.preferred_browser_graph_dir = head

            # export the graph as image file
            export_browser_graph(filename,
                       self.browser_graph_widget.scene)

