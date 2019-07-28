from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, pyqtSlot, QAbstractTableModel, QTimer, QVariant
from PyQt5.QtCore import QModelIndex
from tv_time import t_string

COLUMN_TITLES=["index","filename","file_group","file_size","modtime","file_md5"]

class BrowserFile1TableModel(QAbstractTableModel):

    def __init__(self, all_nodes, parent=None): 
        super(BrowserFile1TableModel, self).__init__()
        self.column_titles = COLUMN_TITLES
        self.all_nodes = all_nodes

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.column_titles[section]
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.all_nodes)

    def columnCount(self, parent=QModelIndex()):
        return len(self.column_titles)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()

            if column == 0:
                return self.all_nodes[row].index
            if column == 1:
                return self.all_nodes[row].filename
            if column == 2:
                return self.all_nodes[row].file_group
            if column == 3:
                return self.all_nodes[row].file_size
            if column == 4:
                return t_string(self.all_nodes[row].modtime)
            if column == 5:
                return self.all_nodes[row].file_md5
            raise RuntimeError("bad")
        else:
            return QVariant()

