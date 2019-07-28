from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox
from math import sqrt

# Provides: tv_sketch_cb

class TVSketchCB(QObject):

    def __init__(self, tv_data_manager):
        super(TVSketchCB, self).__init__()
        self.tv_data_manager = tv_data_manager

        # cb
        self.tv_sketch_cb = QCheckBox("Sketch")
        self.tv_sketch_cb.setToolTip("Draw fast sketch instead of complete")
        self.tv_sketch_cb.setChecked(tv_data_manager.step != 1)
        self.tv_sketch_cb.stateChanged.connect(self._change_check)

    @pyqtSlot(int)
    def _change_check(self, state):
        if state == Qt.Checked:
            is_checked = True
        else:
            is_checked = False
        self.tv_data_manager.toggle_draw_sketch(is_checked)

