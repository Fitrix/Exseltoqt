import numpy
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtGui import Qt, QColor
from PySide6.QtWidgets import QMenu

from sort_on_style import sort_item_vent

class PandasModel(QAbstractTableModel):

    def __init__(self, data, fasonka=True):
        super().__init__()
        self._data = data
        self.fasonka = fasonka

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        # print(index.row())
        # запись пандаc в таблицу
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.iloc[index.row(), index.column()])

        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 1:
            return QColor("#FFFCF1")
        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 2:
            return QColor("#FFE895")
        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 0:
            return QColor("#E6D38E")
        if role == Qt.ItemDataRole.BackgroundRole and index.column() == 3:
            return QColor("#D8CDA7")
        if role == Qt.ItemDataRole.ForegroundRole:
            value = self._data.iloc[index.row()][index.column()]
            if isinstance(value, numpy.int64):
                return QColor("#0A033F")
            if isinstance(value, str):
                return sort_item_vent(value)
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Orientation.Horizontal \
                and role == Qt.ItemDataRole.DisplayRole:
            return self._data.columns[col]
        if self.fasonka:
            if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
                return self._data.axes[0][col]
        return None

    def flags(self, index) -> Qt.ItemFlags:
        return super().flags(index) | Qt.ItemIsSelectable

    def test(self, index):
        print("***", self._data.iloc[index.row(), index.column()])


