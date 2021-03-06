import sys
import board
import bot

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QRadioButton, QGridLayout, QPushButton, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from board import GameHandler


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
        self.white_bot = bot.MinMaxBot(board.WHITE, depth=1)
        self.black_bot = bot.MinMaxBot(board.BLACK, depth=2)
        self.check_boxes = []
        self.bots = [QComboBox(self), QComboBox(self)]
        self.layout = QGridLayout()
        self.game_board = board.GameBoard()
        self.score_label = QLabel(self)
        self.refresh()
        self.score_label.adjustSize()
        self.score_label.move(820, 260+30)
        self.w_depth_line = QLineEdit(self)
        self.w_depth_line.move(820, 220+30)
        self.b_depth_line = QLineEdit(self)
        self.b_depth_line.move(820+150, 220+30)
        self.pieces_on_board = 0
        self.initUI()

    def refresh(self):
        self.score_label.setText(f'WHITE: {GameHandler.get_white_points()} \t\t '
                                 f'BLACK: {GameHandler.get_black_points()}')

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

        depth_w_combo_list = QLabel(self)
        depth_w_combo_list.setText('Depth:')
        depth_w_combo_list.adjustSize()
        depth_w_combo_list.move(820, 200+30)

        depth_b_combo_list = QLabel(self)
        depth_b_combo_list.setText('Depth:')
        depth_b_combo_list.adjustSize()
        depth_b_combo_list.move(820 + 150, 200+30)

        for i in range(2):
            self.bots[i].move(820 + i * 150, 180)
            self.bots[i].addItem('random_bot')
            self.bots[i].addItem('minmax_bot')
            self.bots[i].addItem('alphabeta_bot')
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
        # White bot:
        if self.bots[0].currentText() == 'random_bot':
            self.white_bot = bot.RandomBot(board.WHITE)
        elif self.bots[0].currentText() == 'minmax_bot':
            self.white_bot = bot.MinMaxBot(board.WHITE, int(self.w_depth_line.text()))
        elif self.bots[0].currentText() == 'alphabeta_bot':
            self.white_bot = bot.AlphaBetaBot(board.WHITE, int(self.w_depth_line.text()))
        # White bot:
        if self.bots[1].currentText() == 'random_bot':
            self.black_bot = bot.RandomBot(board.BLACK)
        elif self.bots[1].currentText() == 'minmax_bot':
            self.black_bot = bot.MinMaxBot(board.BLACK, int(self.b_depth_line.text()))
        elif self.bots[1].currentText() == 'alphabeta_bot':
            self.black_bot = bot.AlphaBetaBot(board.BLACK, int(self.b_depth_line.text()))

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
            if response == 'OK':
                bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                bot1_pic.show()
        elif _game_mode == 'BOT_VS_BOT':
            self.game_mode = BOT_VS_BOT
            for i in range(50):
                response, bot_square = self.white_bot.make_a_move()
                bot1_pic = QLabel(self)
                if response == 'OK':
                    bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                    bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                    bot1_pic.show()
                response, bot_square = self.black_bot.make_a_move()
                bot2_pic = QLabel(self)
                if response == 'OK':
                    bot2_pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                    bot2_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                    bot2_pic.show()
        self.refresh()

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
                    if GameHandler.put_white(square) == 'OK':
                        pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                        pic.move(x*80, y*80)
                        pic.show()
                        self.help_value *= -1
                else:
                    if GameHandler.put_black(square) == 'OK':
                        pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                        pic.move(x*80, y*80)
                        pic.show()
                        self.help_value *= -1
            elif self.game_mode == PLAYER_VS_BLACK_BOT:
                if GameHandler.put_white(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                    pic.move(x * 80, y * 80)
                    pic.show()
                    response, bot_square = self.black_bot.make_a_move()
                    if response == 'OK':
                        bot1_pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                        bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                        bot1_pic.show()
            elif self.game_mode == PLAYER_VS_WHITE_BOT:
                if GameHandler.put_black(square) == 'OK':
                    pic.setPixmap(QPixmap("artifacts/black_pawn.png").scaled(80, 80))
                    pic.move(x * 80, y * 80)
                    pic.show()
                    response, bot_square = self.black_bot.make_a_move()
                    if response == 'OK':
                        bot1_pic.setPixmap(QPixmap("artifacts/white_pawn.png").scaled(80, 80))
                        bot1_pic.move(board.SQUARES_CORD[bot_square][0] * 80, board.SQUARES_CORD[bot_square][1] * 80)
                        bot1_pic.show()
        self.refresh()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FreedomApp()
    sys.exit(app.exec_())



