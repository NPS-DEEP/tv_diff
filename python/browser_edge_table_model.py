from PyQt5.QtWidgets import QTableView
from PyQt5.QtCore import Qt, pyqtSlot, QAbstractTableModel, QTimer, QVariant
from PyQt5.QtCore import QModelIndex
from tv_time import t_string

COLUMN_TITLES=["index1","index2","sd","mean","max","sum","max/sum"]
#COLUMN_TITLES=["index","filename","file_group","file_size","modtime","file_md5"]

class BrowserEdgeTableModel(QAbstractTableModel):

    def __init__(self, all_nodes, parent=None): 
        super(BrowserEdgeTableModel, self).__init__()
        self.column_titles = COLUMN_TITLES
        self.all_nodes = all_nodes

        # table's edge records
        self.edge_records = list()

    def set_edge_records(self, edge_records):
        self.beginResetModel()
        self.edge_records = edge_records
        self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.column_titles[section]
        else:
            return QVariant()

    def rowCount(self, parent=QModelIndex()):
        return len(self.edge_records)

    def columnCount(self, parent=QModelIndex()):
        return len(self.column_titles)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            row = index.row()
            column = index.column()

            if column == 0:
                return self.edge_records[row].index1
            if column == 1:
                return self.edge_records[row].index2
            if column == 2:
                return self.edge_records[row].sd
            if column == 3:
                return self.edge_records[row].mean
            if column == 4:
                return self.edge_records[row].maxv
            if column == 5:
                return self.edge_records[row].sumv
            if column == 6:
                return self.edge_records[row].maxv / self.edge_records[row].sumv
            raise RuntimeError("bad")
        else:
            return QVariant()

