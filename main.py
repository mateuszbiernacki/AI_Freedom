import sys
import board

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QGridLayout, QPushButton
from PyQt5.QtGui import QPixmap
from board import GameBoard


# Game modes:
PREGAME = 0
PLAYER_VS_PLAYER = 1
PLAYER_VS_BLACK_BOT = 2
PLAYER_VS_WHITE_BOT = 3
BOT_VS_BOT = 4

GAME_MODES = ['PLAYER_VS_PLAYER', 'PLAYER_VS_BLACK_BOT', 'PLAYER_VS_WHITE_BOT', 'BOT_VS_BOT']


class FreedomApp(QWidget):

    board = GameBoard()

    def __init__(self):
        super().__init__()
        self.title = 'Freedom'
        self.left = 100
        self.top = 100
        self.width = 1300
        self.height = 800
        self.help_value = 1
        self.game_mode = PREGAME
        self.check_boxes = []
        self.layout = QGridLayout()
        self.game_board = board.GameBoard()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        game_modes_label = QLabel(self)
        game_modes_label.setText('Game mode:')
        game_modes_label.adjustSize()
        game_modes_label.move(820, 20)
        play_button = QPushButton(self)
        play_button.clicked.connect(self.play_button_press_action)
        play_button.setText('PLAY')
        play_button.resize(250, 80)
        play_button.move(1000, 50)
        for i in range(len(GAME_MODES)):
            self.check_boxes.append(QRadioButton(self))
            self.check_boxes[i].setText(GAME_MODES[i])
            self.check_boxes[i].move(820, 50 + i * 20)
        # Create board
        label = QLabel(self)
        board_pixmap = QPixmap('artifacts/board.png').scaled(800, 800)
        label.setPixmap(board_pixmap)

        self.setMouseTracking(True)

        self.show()

    def play_button_press_action(self):
        print('play button is pressing')

    def mousePressEvent(self, e):
        x = int(e.x()/80)
        y = int(e.y()/80)
        len_x = len(board.SQUARES_NAMES)
        len_y = len(board.SQUARES_NAMES[0])
        if x < len_x and y < len_y:
            square = board.SQUARES_NAMES[y][x]
            pic = QLabel(self)
            if self.help_value == 1:
                if board.put_white_pawn(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                    pic.move(x*80, y*80)
                    pic.show()
                    self.help_value *= -1
            else:
                if board.put_black_pawn(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                    pic.move(x*80, y*80)
                    pic.show()
                    self.help_value *= -1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FreedomApp()
    sys.exit(app.exec_())
