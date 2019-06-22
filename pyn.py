import sys

from PySide2 import QtCore
from PySide2.QtGui import QCursor, QFont, QFontDatabase, QIcon
from PySide2.QtWidgets import (
    QAction, QApplication, QColorDialog, QDesktopWidget, QFontDialog,
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


class Pyn(QMainWindow):
    def __init__(self, window_title=""):
        super(Pyn, self).__init__()
        # Set size and centre window
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(50, 50, 300, 300)
        qtRectangle = self.frameGeometry()
        print(qtRectangle)
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)

        self.icon = QIcon("icon.png")
        self.move(qtRectangle.topLeft())

        self.setWindowTitle(f"Pyn - {window_title}")
        self.setWindowIcon(self.icon)
        self.setStyleSheet(f"background-color: {YELLOW}")

        self.text_window = CustomLineEdit()  # the actual editor pane
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(24)
        self.text_window.setFont(QFont("Comic Sans MS", 30))
        self.setCentralWidget(self.text_window)

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
    exit()


def new_note():
    global pyn_list
    pyn_list.append(Pyn(window_title="New Note"))


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

    pyn_list.append(Pyn(window_title="Test "))
    app.exec_()


if __name__ == "__main__":
    run()
