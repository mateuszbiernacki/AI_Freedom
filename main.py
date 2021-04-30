import sys
import board

from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from board import GameBoard


class FreedomApp(QWidget):

    board = GameBoard()

    def __init__(self):
        super().__init__()
        self.title = 'Freedom'
        self.left = 100
        self.top = 100
        self.width = 900
        self.height = 900
        self.help_value = 1
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Create board
        label = QLabel(self)
        board_pixmap = QPixmap('artifacts/board.png').scaled(800, 800)
        label.setPixmap(board_pixmap)

        self.setMouseTracking(True)

        self.show()

    def mousePressEvent(self, e):
        x = int(e.x()/80)
        y = int(e.y()/80)
        len_x = len(board.SQUARES_NAMES)
        len_y = len(board.SQUARES_NAMES[0])
        if x < len_x and y < len_y:
            print(board.SQUARES_NAMES[y][x])
            pic = QLabel(self)
            if self.help_value == 1:
                pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
            else:
                pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
            self.help_value *= -1
            pic.move(x*80, y*80)
            pic.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FreedomApp()
    sys.exit(app.exec_())
