
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import qApp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
import os
import ntpath
from version_file import VERSION
from tv_icons import window_icon
from tv_graph_widget import TVGraphWidget
from tv_data_manager import TVDataManager
from settings_manager import SettingsManager, settings
from tv_scale_manager import TVScaleManager
from settings_dialog_wrapper import SettingsDialogWrapper
from export_tv_graph import export_tv_graph
from tv_sketch_cb import TVSketchCB

"""main window containing toolbar and central widget.
"""

class TVMainWindow(QObject):

    # this is the entry point when embedded in tv_browser
    @pyqtSlot(str, str)
    def show_window(self, tv_filename1, tv_filename2):
        self.tv_data_manager.set_tv_data_pair(tv_filename1, tv_filename2)
        self.w.show()

    def __init__(self, signal_edge_selected=None):
        super(TVMainWindow, self).__init__()

        # use this when embedded in tv_browser
        if signal_edge_selected:
            signal_edge_selected.connect(self.show_window)


        # user's preferred TV file path
        self.preferred_tv_dir = os.path.expanduser("~")

        # user's preferred JPG graph path
        self.preferred_graph_dir = os.path.expanduser("~")

        # settings manager
        self.settings_manager = SettingsManager()

        # data manager
        self.tv_data_manager = TVDataManager(settings,
                              self.settings_manager.signal_settings_changed)

        # scale manager
        self.tv_scale_manager = TVScaleManager()

        # main window
        self.w = QMainWindow()

        # main window decoration
        self.w.setGeometry(0,0,950,885)
        self.w.setWindowTitle("Texture Vector Similarity Version %s"%VERSION)
        self.w.setWindowIcon(QIcon(window_icon))

        # the graph main widget
        self.tv_graph_widget = TVGraphWidget(
                              self.tv_data_manager.signal_data_loaded,
                              self.tv_scale_manager.signal_tv_scale_changed)
 
        # the graph
        self.w.setCentralWidget(self.tv_graph_widget.view)

        # actions
        self.define_actions()

        # sketch checkbox
        self.tv_sketch_cb = TVSketchCB(self.tv_data_manager)

        # toolbar
        self.add_toolbar()

    # actions
    def define_actions(self):
        # open file 1
        self.action_open_file1 = QAction(QIcon(
                       "icons/document-open-2.png"), "&Open1...", self)
        self.action_open_file1.setToolTip("Open File 1")
        self.action_open_file1.triggered.connect(self.select_and_open_file1)

        # open file 2
        self.action_open_file2 = QAction(QIcon(
                       "icons/document-open-2.png"), "&Open2...", self)
        self.action_open_file2.setToolTip("Open File 2")
        self.action_open_file2.triggered.connect(self.select_and_open_file2)

        # settings
        self.action_set_settings = QAction(QIcon(
                       "icons/system-settings.png"), "&Settings...", self)
        self.action_set_settings.setToolTip("Manage threshold settings")
        self.action_set_settings.triggered.connect(self.set_settings)

        # draw sketch
        self.action_toggle_draw_sketch = QAction(QIcon(
                       "icons/run-build-2.png"), "&Sketch", self)
        self.action_toggle_draw_sketch.setToolTip(
                                   "Draw fast sketch instead of complete")
        self.action_toggle_draw_sketch.setCheckable(True)
        self.action_toggle_draw_sketch.triggered.connect(
                                   self.tv_data_manager.toggle_draw_sketch)

        # scale in
        self.action_scale_in = QAction(QIcon(
                       "icons/zoom-in-3.png"), "&+", self)
        self.action_scale_in.setToolTip("Scale in")
        self.action_scale_in.triggered.connect(self.tv_scale_manager.scale_in)

        # scale out
        self.action_scale_out = QAction(QIcon(
                       "icons/zoom-out-3.png"), "&-", self)
        self.action_scale_out.setToolTip("Scale out")
        self.action_scale_out.triggered.connect(self.tv_scale_manager.scale_out)

        # scale original size
        self.action_scale_original = QAction(QIcon(
                       "icons/zoom-original-2.png"), "&1", self)
        self.action_scale_original.setToolTip("Scale to original size")
        self.action_scale_original.triggered.connect(
                                         self.tv_scale_manager.scale_original)

        # action export graph as image file
        self.action_export_tv_graph = QAction(QIcon(
                       "icons/document-export-4.png"), "&Export Graph...", self)
        self.action_export_tv_graph.setToolTip("Export similarity graph as image file")
        self.action_export_tv_graph.triggered.connect(
                                     self.select_and_export_tv_graph)

    # toolbar items
    def add_toolbar(self):
        toolbar = self.w.addToolBar("TV Window Toolbar")
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        toolbar.addAction(self.action_open_file1)
        toolbar.addAction(self.action_open_file2)
        toolbar.addAction(self.action_set_settings)
        toolbar.addWidget(self.tv_sketch_cb.tv_sketch_cb)
        toolbar.addAction(self.action_scale_in)
        toolbar.addAction(self.action_scale_out)
        toolbar.addAction(self.action_scale_original)
        toolbar.addAction(self.action_export_tv_graph)

    ############################################################
    # action handlers
    ############################################################

    # Open TV file1
    @pyqtSlot()
    def select_and_open_file1(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self.w,
        "Open Texture Vector file 1",
        self.preferred_tv_dir,
        "TV files (*.tv);;All Files (*)", options=options)

        if filename:
            # remember the preferred path
            head, tail = os.path.split(filename)
            self.preferred_tv_dir = head

            # read the file into tv_data1
            self.tv_data_manager.set_tv_data1(filename)

    # Open TV file2
    @pyqtSlot()
    def select_and_open_file2(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self.w,
        "Open Texture Vector file 2",
        self.preferred_tv_dir,
        "TV files (*.tv);;All Files (*)", options=options)

        if filename:
            # remember the preferred path
            head, tail = os.path.split(filename)
            self.preferred_tv_dir = head

            # read the file into tv_data2
            self.tv_data_manager.set_tv_data2(filename)

    # set settings
    @pyqtSlot()
    def set_settings(self):
        wrapper = SettingsDialogWrapper(self.w, self.settings_manager)
        wrapper.exec_()

    def suggested_tv_graph_filename(self):
        try:
            name1 = "_%s"%ntpath.basename(
                                 self.tv_data_manager.tv_data1["filename"])
        except Exception:
            name1 = ""
        try:
            name2 = "_%s"%ntpath.basename(
                                 self.tv_data_manager.tv_data2["filename"])
        except Exception:
            name2 = ""

        return "tv_graph%s%s.png"%(name1, name2)

    # export graph as image file
    @pyqtSlot()
    def select_and_export_tv_graph(self):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # suggested filename
        suggested_filename = self.suggested_tv_graph_filename()

        filename, _ = QFileDialog.getSaveFileName(self.w,
        "Export graph image file",
        os.path.join(self.preferred_graph_dir, suggested_filename),
        "TV graph image files (*.png);;All Files (*)", options=options)

        if filename:
            # remember the preferred path
            head, _tail = os.path.split(filename)
            self.preferred_graph_dir = head

            # export the graph as image file
            export_tv_graph(filename, self.tv_graph_widget.scene)

