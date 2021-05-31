import random
import board

from main import GameHandler


class Bot:
    def __init__(self, color):
        self.color = ''
        if color == board.BLACK:
            self.color = 'black'
        elif color == board.WHITE:
            self.color = 'white'

    def make_a_move(self):
        pass


class RandomBot(Bot):
    def make_a_move(self):
        possible_movies = GameHandler.get_possible_movies()
        if len(possible_movies) == 0:
            _board = GameHandler.get_board()
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        random_index = random.randint(0, len(possible_movies)-1)
        move = possible_movies[random_index]
        # print(possible_movies)
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        return 'OK', move

