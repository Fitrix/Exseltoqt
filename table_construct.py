from PySide6.QtGui import Qt
from PySide6.QtWidgets import QListWidget


class TableQt(QListWidget):
    def __init__(self):
        super().__init__()

        # self.setDragDropMode(QAbstractItemView.DragOnly)
        self.setDefaultDropAction(Qt.IgnoreAction)

        self.setStyleSheet("QListWidget {background-color: #d1dcda; }")

    # def startDrag(self, supported_actions: Qt.DropActions) -> None:
    #
    #     item = self.selectedItems()
    #
    #     drag = QDrag(self)
    #     mimedata = self.mimeData(item)
    #     mimedata.setProperty("D:\MyPy\ventProject", item)
    #
    #     drag.setMimeData(mimedata)
    #     drag.exec(supported_actions)
    #     print(item)
