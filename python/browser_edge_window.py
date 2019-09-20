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

from browser_edge_table_model import BrowserEdgeTableModel

"""Open browser edge main window."""

class BrowserEdgeWindow(QObject):

    def __init__(self, all_nodes, change_manager):
        super(BrowserEdgeWindow, self).__init__()

        self.all_nodes = all_nodes
        self.change_manager = change_manager

        # main window
        self.w = QMainWindow()

        # main window decoration
        self.w.setGeometry(0,0,610,900)
        self.w.setWindowTitle("Open Similarity Edge")
        self.w.setWindowIcon(QIcon(window_icon))
        self.w.setWindowModality(Qt.ApplicationModal)

        # the browser edge table model
        self.browser_edge_table_model = BrowserEdgeTableModel(all_nodes)

        # the proxy model
        self.proxy_model = QSortFilterProxyModel()

        # the browser edge table
        self.browser_edge_table = QTableView()
        self.browser_edge_table.setSortingEnabled(True)
        self.browser_edge_table.setSelectionBehavior(
                                         QAbstractItemView.SelectRows)
        self.browser_edge_table.setSelectionMode(
                                         QAbstractItemView.SingleSelection)
        self.browser_edge_table.clicked.connect(self._select_index)
        self.proxy_model.setSourceModel(self.browser_edge_table_model)
        self.browser_edge_table.setModel(self.proxy_model)
        self.w.setCentralWidget(self.browser_edge_table)
 
    def show_window(self, edge_records):
        self.browser_edge_table_model.set_edge_records(edge_records)
        self.w.show()

    @pyqtSlot(QModelIndex)
    def _select_index(self, model_index):
        list_index = self.proxy_model.mapToSource(model_index).row()
        edge_record=self.browser_edge_table_model.edge_records[list_index]
        node_record1 = self.all_nodes[edge_record.index1-1]
        node_record2 = self.all_nodes[edge_record.index2-1]
        print("Open similarity edge")
        print(edge_record.text())
        self.change_manager.edge_selected_event(edge_record,
                                                node_record1, node_record2)
        self.w.hide()

