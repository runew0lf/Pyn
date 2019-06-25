import sys
import json

from PySide2 import QtCore
from PySide2.QtGui import QCursor, QFont, QFontDatabase, QIcon, QPalette
from PySide2.QtWidgets import (QAction, QApplication, QColorDialog,
                               QDesktopWidget, QDialog, QFontDialog,
                               QMainWindow, QMenu, QSystemTrayIcon, QTextEdit)

YELLOW = "#EDE976"

pyn_list = []

"""
TODO:
Save notes
Change context menu's to show notes - maybe?
Change note title
"""


class CustomLineEdit(QTextEdit):
    def __init__(self, parent=None):
        super(CustomLineEdit, self).__init__()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)

    def __contextMenu(self):
        # self._normalMenu = self.createStandardContextMenu() # Remove this for standard menu
        self._normalMenu = QMenu()
        self._addCustomMenuItems(self._normalMenu)
        self._normalMenu.exec_(QCursor.pos())

    def _addCustomMenuItems(self, menu):
        # menu.addSeparator() # add a seperator
        menu.addAction("Change Colour", self.colourchange)
        menu.addAction("Change Font", self.changefont)
        menu.addAction("Edit Title", self.changetitle)

    def changetitle(self):
        popup = ExamplePopup(self)
        popup.setGeometry(100, 200, 100, 100)
        popup.exec_()

    def changefont(self):
        dialog = QFontDialog()
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dialog.exec()
        font = dialog.selectedFont()
        self.setFont(font)

    def colourchange(self):
        dialog = QColorDialog()
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dialog.exec()
        color = dialog.selectedColor()
        self.setStyleSheet(f"background-color: {color.name()}")


class ExamplePopup(QDialog):
    def __init__(self, name="test", parent=None):
        super().__init__(parent)
        self.name = name
        self.label = QTextEdit(self)
        self.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )


class Pyn(QMainWindow):
    def __init__(self, saved_data=None):
        super(Pyn, self).__init__()
        # Set size and centre window
        # "text": pyn.text_window.toPlainText(),

        if saved_data is None:
            self.setGeometry(50, 50, 300, 300)
            qtRectangle = self.frameGeometry()
            centerPoint = QDesktopWidget().availableGeometry().center()
            qtRectangle.moveCenter(centerPoint)
            self.move(qtRectangle.topLeft())
            self.setStyleSheet(f"background-color: {YELLOW}")
        else:
            rect = saved_data['rect']
            rect[3] -= 32
            self.setGeometry(*rect)
            self.setStyleSheet(f"background-color: {saved_data['background']}")

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.icon = QIcon("icon.png")
        self.setWindowIcon(self.icon)
        self.setWindowTitle(f"Pyn")
        self.text_window = CustomLineEdit()  # the actual editor pane
        self.setCentralWidget(self.text_window)

        if saved_data is None:
            self.text_window.setFont(QFont("Comic Sans MS", 30))
        else:
            self.text_window.setFont(QFont(saved_data['font'], saved_data['font_size']))
            self.text_window.setText(saved_data['text'])

        self.show()

    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        global pyn_list
        pyn_list.remove(self)

    # Check for minimized window and hide it
    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                self.setWindowState(QtCore.Qt.WindowNoState)
                self.hide()


# Restore view when tray icon doubleclicked
def systemIcon(reason):
    if reason == QSystemTrayIcon.DoubleClick:
        show_all()


def setup_app(app):
    # Stop window closing
    app.setQuitOnLastWindowClosed(False)

    # Init QSystemTrayIcon
    icon = QIcon("icon.png")
    tray_icon = QSystemTrayIcon(app)
    tray_icon.setIcon(icon)

    # Add Menu Actions to App
    new_action = QAction("New", app)
    show_action = QAction("Show All", app)
    hide_action = QAction("Hide All", app)
    quit_action = QAction("Exit", app)

    new_action.triggered.connect(new_note)
    show_action.triggered.connect(show_all)
    hide_action.triggered.connect(hide_all)
    quit_action.triggered.connect(quit_app)

    # Add Tray Menu
    tray_menu = QMenu()
    tray_menu.addAction(new_action)
    tray_menu.addAction(show_action)
    tray_menu.addAction(hide_action)
    tray_menu.addAction(quit_action)
    tray_icon.setContextMenu(tray_menu)
    tray_icon.activated.connect(systemIcon)
    tray_icon.show()


def quit_app():
    global pyn_list
    json_data = []
    for pyn in pyn_list:
        pyn_data = {
        "text": pyn.text_window.toPlainText(),
        "background": pyn.text_window.palette().color(QPalette.Background).name(),
        "rect": pyn.frameGeometry().getRect(),
        "font": pyn.text_window.currentFont().family(),
        "font_size": pyn.text_window.currentFont().pointSize()
        }
        json_data.append(pyn_data)
    with open('data.json', 'w') as outfile:
        json.dump(json_data, outfile)
    exit()


def new_note():
    global pyn_list
    pyn_list.append(Pyn())


def show_all():
    global pyn_list
    for note in pyn_list:
        note.show()


def hide_all():
    global pyn_list
    for note in pyn_list:
        note.hide()


def run():
    global pyn_list

    app = QApplication(sys.argv)
    setup_app(app)

    with open('data.json') as json_file:  
        data = json.load(json_file)
        for note in data:
            # pyn_list.append(Pyn())
            pyn_list.append(Pyn(saved_data=note))
    app.exec_()


if __name__ == "__main__":
    run()
