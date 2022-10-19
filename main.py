import os
import sys

from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from mainWindow import Window


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
def checkFileEnding():
    if os.path.exists("progectNumber.txt"):
        with open("progectNumber.txt", "r", encoding="utf-8") as f:
            l = sum(1 for _ in f)
    else:
        with open("progectNumber.txt", "w", encoding="utf-8") as f:
            f.write(" \n")
            l = 0
    return l


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # checkFileEnding()
    print_hi('PyCharm')
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    if checkFileEnding() > 100:
        QMessageBox.critical(QDialog(), "The End", "oops, no working")
        sys.exit()

    sys.exit(app.exec())
