import sys

from PySide2.QtGui import QFont, QIcon, QFontDatabase, QCursor, QColor
from PySide2 import QtCore
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QDesktopWidget,
    QTextEdit,
    QMainWindow,
    QMenu,
    QSystemTrayIcon,
    qApp,
    QColorDialog,
)

YELLOW = "#EDE976"

pyn_list = []

"""
TODO: 
Save notes
Change context menu's to show notes
Change note title
Change font
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

    def colourchange(self):
        dialog = QColorDialog()
        dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        dialog.exec()
        color = dialog.selectedColor()
        self.setStyleSheet(f"background-color: {color.name()}")


class Window(QMainWindow):
    def __init__(self, window_title=""):
        super(Window, self).__init__()
        # Set size and centre window
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(50, 50, 300, 300)
        qtRectangle = self.frameGeometry()
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


    #Check for minimized window and hide it    
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
    with open("pyn.data", "wb") as pickle_data:
        pickle.dump(pyn_list, pickle_data)
    qApp.quit

def new_note():
    global pyn_list
    pyn_list.append(Window(window_title="New Note"))


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

    pyn_list.append(Window(window_title="Test "))

    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass


if __name__ == "__main__":
    run()
