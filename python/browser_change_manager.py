from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSignal, pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from browser_graph_data_reader import NodeRecord, EdgeRecord
from browser_tv_filename import browser_tv_filename

"""Provides several browser signal services."""

# browser graph scale
browser_original_scale = 1.0 # const

# SettingsManager signals change: file1 index, threshold, in_group
class BrowserChangeManager(QObject):

    # signal
    signal_inputs_changed = pyqtSignal(NodeRecord, float, bool,
                                                          name='inputsChanged')
    signal_node_hovered = pyqtSignal(NodeRecord, name='nodeHovered')
    signal_edge_hovered = pyqtSignal(EdgeRecord, NodeRecord, NodeRecord,
                                                          name='edgeHovered')
    signal_edge_selected = pyqtSignal(str, str, name='edgeSelected')
    signal_browser_scale_changed = pyqtSignal(float, name='BrowserScaleChanged')

    def __init__(self, node_record1, threshold, in_group):
        super(BrowserChangeManager, self).__init__()

        self._scale = browser_original_scale

        self.node_record1 = node_record1
        self.threshold = threshold
        self.in_group = in_group
        self._emit()

    def _emit(self):
        self.signal_inputs_changed.emit(self.node_record1,
                                        self.threshold, self.in_group)

    # called from browser main window handler, similarity gaph
    def change_node_record1(self, node_record1):
        self.node_record1 = node_record1
        self._emit()

    # called from threshold_slider
    @pyqtSlot(float)
    def change_threshold(self, threshold):
        self.threshold = threshold
        self._emit()

    # called from browser main window handler
    def change_in_group(self, in_group):
        self.in_group = in_group
        self._emit()

    # called from g_edge to signal file pair selection
    def edge_selected_event(self, edge_record, node_record_a, node_record_b):

        # make ordering reflect order in edge
        if edge_record.index1 == node_record_b.index:
            node_record_a,node_record_b = node_record_b,node_record_a

        tv_filename1 = browser_tv_filename(node_record_a.file_md5)
        tv_filename2 = browser_tv_filename(node_record_b.file_md5)
        self.signal_edge_selected.emit(tv_filename1, tv_filename2)

    # scale
    def scale_in(self):
        self._scale *=2.0
        # signal change
        self.signal_browser_scale_changed.emit(self._scale)

    def scale_out(self):
        self._scale /=2.0
        # signal change
        self.signal_browser_scale_changed.emit(self._scale)

    def scale_original(self):
        self._scale = browser_original_scale
        # signal change
        self.signal_browser_scale_changed.emit(self._scale)

