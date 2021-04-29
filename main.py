import sys
import board

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap


class FreedomApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freedom'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 900
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create board
        label = QLabel(self)
        board_pixmap = QPixmap('artifacts/board.png').scaled(800, 800)
        label.setPixmap(board_pixmap)
        #self.resize(board_pixmap.width(), board_pixmap.height())

        self.setMouseTracking(True)

        self.show()

    def mousePressEvent(self, e):
        x = e.x()
        y = e.y()

        print(f'x: {x},  y: {y}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FreedomApp()
    sys.exit(app.exec_())
