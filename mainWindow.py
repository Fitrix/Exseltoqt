import os
import time

import pandas as pd
from PySide6.QtCore import QObject, QEvent

from PySide6.QtGui import Qt, QIcon, QMovie, QColor, QAction
from PySide6.QtWidgets import QWidget, QHBoxLayout, QTableView, QLabel, QPushButton, QMessageBox, QDialog, \
    QListWidgetItem, QFileDialog, QMenu, QColorDialog
from openpyxl import load_workbook

from pasre_flance import count_time
from refact_xls import refactXls
from table_Qt import PandasModel
from table_construct import TableQt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        # self.fileName = os.path.dirname(__file__)
        self.fileName = []
        self.read_list_file()
        self.df = None

        self.setWindowFlags(Qt.WindowType.Dialog)
        self.setWindowIcon(QIcon("images\cart-cat.ico"))

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.viewWindow = TableQt()
        self.viewWindow.installEventFilter(self)

        self.view = QTableView()

        self.view.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.WindowStaysOnTopHint)

        # self.view.setWindowIcon(QIcon("hammer.ico"))
        self.viewWindow.setWindowIcon(QIcon('images\Raspberry.ico'))

        self.layout.addWidget(self.viewWindow)
        # self.view.resize(100, 200)

        self.setWindowTitle("Testing 0.9.77")
        self.setFixedSize(320, 270)

        self.movie_laber = QLabel(self)
        self.movie = QMovie("images\cats-3.gif")
        self.movie_laber.setMovie(self.movie)
        self.movie.start()
        self.layout.addWidget(self.movie_laber)

        self.button_open_pj = QPushButton('Open Project', self)
        self.button_open_pj.move(190, 215)
        self.button_open_pj.setStyleSheet('QPushButton {background-color: rgba(202, 215, 215, 0); '
                                          'color: #423f24; border-radius:5px;'
                                          'font: 99 10pt "Arial";} '
                                          'QPushButton:hover {background-color: rgba(220, 55, 10, 50); '
                                          'color: #423f24; border-radius:15px;'
                                          'font: 57 11pt "Arial";}'
                                          'QPushButton:pressed {background-color: rgba(110, 215, 215, 40); '
                                          'color: #423f24; border-radius:12px; '
                                          'font: 557 9pt "Arial";} ')
        self.button_open_pj.clicked.connect(self.open_pandas)

        self.button_flanc2 = QPushButton("Обновить", self)
        self.button_flanc2.resize(70, 25)
        self.button_flanc2.move(165, 245)
        self.button_flanc2.setStyleSheet('QPushButton {background-color: rgba(110, 215, 215, 40); '
                                         'color: #423f24; border-radius:5px; '
                                         'font: 557 10pt "Arial";} '
                                         'QPushButton:hover {background-color: rgba(210, 215, 115, 120); '
                                         'color: #423f24; border-radius:12px; '
                                         'font: 57 11pt "Arial";} '
                                         'QPushButton:pressed {background-color: rgba(110, 215, 215, 40); '
                                         'color: #423f24; border-radius:12px; '
                                         'font: 557 9pt "Arial";} ')

        self.button_flanc2.pressed.connect(self.add_path_names)

        self.button_flanc = QPushButton("Выбрать", self)
        self.button_flanc.resize(70, 25)
        self.button_flanc.move(240, 245)
        self.button_flanc.setStyleSheet('QPushButton {background-color: rgba(110, 215, 215, 40); '
                                        'color: #423f24; border-radius:5px;'
                                        'font: 557 10pt "Arial";} '
                                        'QPushButton:hover {background-color: rgba(220, 195, 100, 90); '
                                        'font: 57 11pt "Arial";}'
                                        'QPushButton:pressed {background-color: rgba(110, 215, 215, 40); '
                                        'color: #423f24; border-radius:12px; '
                                        'font: 557 9pt "Arial";} ')
        self.button_flanc.clicked.connect(self.openFileNameDialog)

        self.viewWindow.itemSelectionChanged.connect(self.onClicked)
        self.viewWindow.itemDoubleClicked.connect(self.open_pandas)

    def add_path_names(self):
        try:
            self.viewWindow.clear()
            with open("path_name_file.txt", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if line.strip():
                        for item in sorted(os.listdir(line.replace("\n", ""))):
                            if ".." in item or "гот." in item:
                                item = self.setColorItem(item, "#7fc896")
                            elif ".xls" in item:
                                item = self.setColorItem(item, Qt.black)
                            elif ".dxf" in item:
                                item = self.setColorItem(item, "#314bde")
                            else:
                                item = self.setColorItem(item, "#af9a9f")
                            self.viewWindow.addItem(item)
        except FileNotFoundError:
            QMessageBox.critical(QDialog(), "              АшuбкО",
                                 "        Включи Internet\n                 или\n Укажи папку правильно")

    def openFileNameDialog(self):
        self.create_list_file(QFileDialog.getExistingDirectory(self, "Добавить папку"))
        self.add_path_names()

    # @count_time
    def onClicked(self):
        ws = None
        self.df = []
        if self.viewWindow.selectedItems():
            item = self.viewWindow.selectedItems()[0].text()
            for path in self.fileName:
                if item in os.listdir(path):
                    if item.split(".")[-1] == "xls":
                        if item + "x" not in os.listdir("xls_projects"):
                            df1 = pd.read_excel(f"{path}/{item}", header=None)
                            df1.to_excel(f"xls_projects/{item}x", index=False, header=False)
                        wb = load_workbook(f"xls_projects/{item}x")
                        ws = wb.active
        if ws:
            self.df = refactXls(ws)

    def open_pandas(self):
        try:
            name_list = self.viewWindow.selectedItems()[0].text().split('.')
            if name_list[-1] == "xls":
                name = f"{name_list[0]}    {self.df[3][0]}"
                model = PandasModel(self.df[0], fasonka=False)
                self.view.setWindowIcon(QIcon('images\Raspberry.ico'))
                self.view.setModel(model)
                self.view.setWindowTitle(name)
                self.view.resize(600, 600)
                self.view.resizeColumnsToContents()
                self.view.show()


                with open("progectNumber.txt", "r+", encoding="utf-8") as f:
                    if name not in f.read():
                        f.write(f"{name}    - -- -  {time.strftime('%Y-%m-%d', time.localtime())}\n")
        except IndexError:
            QMessageBox.critical(QDialog(), "IndexError", "Не тот формат")
        except:
            QMessageBox.critical(QDialog(), "АшибкО", "Не тот формат")

    def open_flance_pandas(self):
        if self.df:
            model = PandasModel(self.df[1])
            self.view.setWindowTitle(f"{self.viewWindow.selectedItems()[0].text().split('.')[0]}  Трубы")
            self.view.setModel(model)
            self.view.resize(150, 300)
            self.view.resizeColumnsToContents()
            self.view.show()

    def open_flance_pandas_fasonka(self):
        if self.df:
            model = PandasModel(self.df[2])
            self.view.setWindowTitle(f"{self.viewWindow.selectedItems()[0].text().split('.')[0]}  Фасонка")
            self.view.setModel(model)
            self.view.resize(150, 300)
            self.view.resizeColumnsToContents()
            self.view.show()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.ContextMenu and watched is self.viewWindow:
            menu = QMenu()
            filename = os.path.abspath(self.get_name_file()[1])
            rename_file = QAction("Гот", self)
            colorSet = QAction("Set Color", self)
            folder_open = QAction("Открыть папку", self)
            fason = QAction("Фасонка", self)
            tube = QAction("Короба", self)
            rename_file.triggered.connect(lambda x: self.rename_files(watched, event, filename))
            tube.triggered.connect(self.open_flance_pandas)
            fason.triggered.connect(self.open_flance_pandas_fasonka)
            colorSet.triggered.connect(self.set_color)
            folder_open.triggered.connect(lambda x: os.startfile(filename))

            # self.cAct.setShortcut(QCoreApplication.translate("MainWindow", "Ctrl+s"))
            menu.addAction(rename_file)
            menu.addAction(folder_open)
            menu.addAction(fason)
            menu.addAction(tube)
            menu.addAction(colorSet)

            menu.exec(event.globalPos())
            # if menu.exec(event.globalPos()):
            #     item = watched.itemAt(event.pos()).text()
            # if item.split(".")[-1] == "dxf":
            #     print(item)
            #     pass

            return True
        return super().eventFilter(watched, event)

    def rename_files(self, watched, event, file):
        try:
            item = watched.itemAt(event.pos())
            fake_item = item.text().split(".")[0] + " гот." + item.text().split(".")[1]
            if item.text().split()[0] + "x" in os.listdir("xls_projects"):
                if fake_item not in os.listdir("xls_projects"):
                    for filename in os.listdir("xls_projects"):
                        if filename == item.text() + "x":
                            old_name = str(file + "/" + item.text()).replace("/", "\\")
                            new_name = str(file + "/" + fake_item).replace("/", "\\")
                            os.rename(old_name, new_name)
                            self.onClicked()
        except IndexError:
            QMessageBox.critical(QDialog(), "Bug", "Не тот File")

    def create_list_file(self, name_file):
        if os.path.exists("path_name_file.txt"):
            with open("path_name_file.txt", "r", encoding="utf-8") as f:
                if name_file not in f.read():
                    with open("path_name_file.txt", "a", encoding="utf-8") as f2:
                        f2.write(name_file + "\n")
        else:
            with open("path_name_file.txt", "w", encoding="utf-8") as f:
                f.write(name_file + "\n")
        self.read_list_file()

    def read_list_file(self):
        if os.path.exists("path_name_file.txt"):
            with open("path_name_file.txt", "r", encoding="utf-8") as f:
                for path in f.readlines():
                    self.fileName.append(path.strip())

    def get_name_file(self):
        if self.viewWindow.selectedItems():
            item = self.viewWindow.selectedItems()[0].text()
            for path in self.fileName:
                if item in os.listdir(path):
                    return [item, path]

    @staticmethod
    def setColorItem(item, color):
        item: QListWidgetItem = QListWidgetItem(item)
        item.setForeground(QColor(color))
        return item

    def set_color(self):
        color_item = QColorDialog.getColor(QColor(222, 222, 222), QDialog(), "...Тык...")
        return color_item

