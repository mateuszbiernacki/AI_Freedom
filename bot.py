import random
import board

from main import GameHandler
from board import GameBoard


class Bot:
    def __init__(self, color, depth=2):
        self.color = ''
        self.depth = depth
        if color == board.BLACK:
            self.color = 'black'
        elif color == board.WHITE:
            self.color = 'white'
        if self.color == 'white':
            self._color = board.WHITE
            self._opponent_color = board.BLACK
        elif self.color == 'black':
            self._opponent_color = board.WHITE
            self._color = board.BLACK

    def make_a_move(self, game_board: GameBoard):
        pass


class RandomBot(Bot):
    def make_a_move(self, game_board: GameBoard):
        possible_movies = GameHandler.get_possible_movies()
        print(possible_movies)
        if len(possible_movies) == 0:
            _board = GameHandler.get_board()
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        random_index = random.randint(0, len(possible_movies) - 1)
        move = possible_movies[random_index]
        # print(possible_movies)
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        return 'OK', move


class MinMaxBot(Bot):

    def make_a_move(self, game_board: GameBoard):
        possible_movies = GameHandler.get_possible_movies()
        if len(possible_movies) == 0:
            _board = GameHandler.get_board()
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        # random_index = random.randint(0, len(possible_movies) - 1)
        # move = possible_movies[random_index]
        move = self.min_max(GameHandler.game_board, self.depth, self._color, self._opponent_color)[0]
        # print(possible_movies)
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        return 'OK', move

    def min_max(self, game_board: GameBoard, depth, current_color, next_color):
        if current_color == self._color:
            best_move = ['', -1000]
        else:
            best_move = ['', 1000]
        for possible_move in game_board.possible_next_movies:
            if depth == 0:
                white_points = int(game_board.count_current_result(board.WHITE))
                black_points = int(game_board.count_current_result(board.BLACK))
                if self._color == board.WHITE:
                    return [possible_move, white_points - black_points]

                elif self._color == board.BLACK:
                    return [possible_move, black_points - white_points]

            fake_game_board = GameBoard()
            fake_game_board.board = game_board.board.copy()
            fake_game_board.last_move = game_board.last_move.copy()
            fake_game_board.possible_next_movies = game_board.possible_next_movies.copy()
            if len(fake_game_board.possible_next_movies) == 0:
                _board = GameHandler.get_board()
                for square in _board:
                    if _board[square] == 0:
                        fake_game_board.possible_movies.append(square)
            fake_game_board.empty_squares = game_board.empty_squares
            fake_game_board.history_of_moves = game_board.history_of_moves[:]
            fake_game_board.next_color = game_board.next_color
            fake_game_board.put_piece(current_color, next_color, possible_move)
            result = [possible_move, self.min_max(fake_game_board, depth - 1, next_color, current_color)[1]]
            # Bot turn -> max
            if current_color == self._color:
                if result[1] > best_move[1]:
                    best_move = result
            # Opponent turn -> min
            elif current_color == self._opponent_color:
                if result[1] < best_move[1]:
                    best_move = result
        print(best_move)
        return best_move
