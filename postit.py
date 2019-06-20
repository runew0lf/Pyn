import sys

from PySide2.QtGui import QFont, QIcon, QFontDatabase
from PySide2.QtWidgets import (QAction, QApplication, QDesktopWidget, QPlainTextEdit,
                               QMainWindow, QMenu, QSystemTrayIcon, qApp, QWidget)

YELLOW = "#EDE976"


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        # Set size and centre window
        self.setGeometry(50, 50, 300, 300)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)

        self.icon = QIcon("icon.png")
        self.move(qtRectangle.topLeft())

        self.setWindowTitle("Python Post-It")
        self.setWindowIcon(self.icon)
        self.setStyleSheet(f"background-color: {YELLOW}")

        self.home()

    def home(self):
        self.text_window = QPlainTextEdit()  # the actual editor pane
        self.text_window.setTabStopWidth(800)  # Set the tabstop to a nice pretty 800 pixels
        fixed_font = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPointSize(24)
        self.text_window.setFont(QFont('Comic Sans MS', 30))
        self.setCentralWidget(self.text_window)    
        # Init QSystemTrayIcon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.icon)

        # Add Menu Actions
        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)
        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        # Add Tray Menu
        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.systemIcon)
        self.tray_icon.show()

        self.show()

    # Restore view when tray icon doubleclicked
    def systemIcon(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    GUI.setVisible(True)
    NEWGUI = Window()
    NEWGUI.setVisible(True)    
    try:
        sys.exit(app.exec_())
    except SystemExit:
        pass


if __name__ == "__main__":
    run()
