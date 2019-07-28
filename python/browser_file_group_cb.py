from PyQt5.QtCore import QObject # for signal/slot support
from PyQt5.QtCore import pyqtSlot # for signal/slot support
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCheckBox

# Provides: browser_file_group_cb

class BrowserFileGroupCB(QObject):

    def __init__(self, change_manager):
        super(BrowserFileGroupCB, self).__init__()
        self.change_manager = change_manager

        # cb
        self.browser_file_group_cb = QCheckBox("Stay in group")
        self.browser_file_group_cb.setToolTip("Only compare files "
                                      "within the opened file group")
        self.browser_file_group_cb.setChecked(change_manager.in_group)
        self.browser_file_group_cb.stateChanged.connect(self._change_check)

    @pyqtSlot(int)
    def _change_check(self, state):
        if state == Qt.Checked:
            in_group = True
        else:
            in_group = False
        self.change_manager.change_in_group(in_group)

