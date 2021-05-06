import subprocess
import sys
import board
import bot
import time

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QGridLayout, QPushButton, QComboBox
from PyQt5.QtGui import QPixmap
from board import game_board


# Game modes:
PREGAME = 0
PLAYER_VS_PLAYER = 1
PLAYER_VS_BLACK_BOT = 2
PLAYER_VS_WHITE_BOT = 3
BOT_VS_BOT = 4

GAME_MODES = ['PLAYER_VS_PLAYER', 'PLAYER_VS_BLACK_BOT', 'PLAYER_VS_WHITE_BOT', 'BOT_VS_BOT']


class FreedomApp(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Freedom'
        self.left = 100
        self.top = 100
        self.width = 1300
        self.height = 800
        self.help_value = 1
        self.game_mode = PREGAME
        self.white_bot = bot.RandomBot(board.WHITE)
        self.black_bot = bot.RandomBot(board.BLACK)
        self.check_boxes = []
        self.bots = [QComboBox(self), QComboBox(self)]
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
        white_bot_combo_list = QLabel(self)
        white_bot_combo_list.setText('White bot')
        white_bot_combo_list.adjustSize()
        white_bot_combo_list.move(820, 160)
        black_bot_combo_list = QLabel(self)
        black_bot_combo_list.setText('Black bot')
        black_bot_combo_list.adjustSize()
        black_bot_combo_list.move(820+150, 160)
        for i in range(2):
            self.bots[i].move(820 + i * 150, 180)
            self.bots[i].addItem('random_bot')
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
        _game_mode = ''
        for mode in self.check_boxes:
            if mode.isChecked():
                _game_mode = mode.text()

        if _game_mode == 'PLAYER_VS_PLAYER':
            self.game_mode = PLAYER_VS_PLAYER
        elif _game_mode == 'PLAYER_VS_BLACK_BOT':
            self.game_mode = PLAYER_VS_BLACK_BOT
        elif _game_mode == 'PLAYER_VS_WHITE_BOT':
            self.game_mode = PLAYER_VS_WHITE_BOT
            response, bot_square = self.white_bot.make_a_move()
            bot1_pic = QLabel(self)
            print(board.game_board.possible_next_movies)
            if response == 'OK':
                bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                bot1_pic.show()
        elif _game_mode == 'BOT_VS_BOT':
            self.game_mode = BOT_VS_BOT
            for i in range(50):
                response, bot_square = self.white_bot.make_a_move()
                bot1_pic = QLabel(self)
                print(board.game_board.possible_next_movies)
                if response == 'OK':
                    bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                    bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                    bot1_pic.show()
                response, bot_square = self.black_bot.make_a_move()
                bot2_pic = QLabel(self)
                print(board.game_board.possible_next_movies)
                if response == 'OK':
                    bot2_pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                    bot2_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                    bot2_pic.show()

    def mousePressEvent(self, e):
        x = int(e.x()/80)
        y = int(e.y()/80)
        len_x = len(board.SQUARES_NAMES)
        len_y = len(board.SQUARES_NAMES[0])
        if x < len_x and y < len_y:
            square = board.SQUARES_NAMES[y][x]
            pic = QLabel(self)
            bot1_pic = QLabel(self)
            if self.game_mode == PREGAME:
                return
            elif self.game_mode == PLAYER_VS_PLAYER:
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
            elif self.game_mode == PLAYER_VS_BLACK_BOT:
                if board.put_white_pawn(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                    pic.move(x * 80, y * 80)
                    pic.show()
                    response, bot_square = self.black_bot.make_a_move()
                    print(board.game_board.possible_next_movies)
                    if response == 'OK':
                        bot1_pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                        bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                        bot1_pic.show()
            elif self.game_mode == PLAYER_VS_WHITE_BOT:
                if board.put_black_pawn(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                    pic.move(x * 80, y * 80)
                    pic.show()
                    response, bot_square = self.black_bot.make_a_move()
                    print(board.game_board.possible_next_movies)
                    if response == 'OK':
                        bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                        bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                        bot1_pic.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FreedomApp()
    sys.exit(app.exec_())



