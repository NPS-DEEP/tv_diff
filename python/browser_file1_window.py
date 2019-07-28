from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableView
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QSortFilterProxyModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from tv_icons import window_icon

from browser_file1_table_model import BrowserFile1TableModel

"""Open browser File1 main window."""

class BrowserFile1Window(QObject):

    def __init__(self, all_nodes, change_manager):
        super(BrowserFile1Window, self).__init__()

        self.all_nodes = all_nodes
        self.change_manager = change_manager

        # main window
        self.w = QMainWindow()

        # main window decoration
        self.w.setGeometry(0,0,800,900)
        self.w.setWindowTitle("Open TV File")
        self.w.setWindowIcon(QIcon(window_icon))
        self.w.setWindowModality(Qt.ApplicationModal)

        # the browser file1 table model
        self.browser_file1_table_model = BrowserFile1TableModel(all_nodes)

        # the proxy model
        self.proxy_model = QSortFilterProxyModel()

        # the browser file1 table
        self.browser_file1_table = QTableView()
        self.browser_file1_table.setSortingEnabled(True)
        self.browser_file1_table.setSelectionBehavior(
                                         QAbstractItemView.SelectRows)
        self.browser_file1_table.setSelectionMode(
                                         QAbstractItemView.SingleSelection)
        self.browser_file1_table.clicked.connect(self._select_index)
        self.proxy_model.setSourceModel(self.browser_file1_table_model)
        self.browser_file1_table.setModel(self.proxy_model)
        self.w.setCentralWidget(self.browser_file1_table)
 
    def show_window(self):
        self.w.show()

    @pyqtSlot(QModelIndex)
    def _select_index(self, model_index):
        list_index = self.proxy_model.mapToSource(model_index).row()
        node_record=self.all_nodes[list_index]
        print("_select_index")
        print(node_record.text())
        self.change_manager.change_node_record1(node_record)
        self.w.hide()

