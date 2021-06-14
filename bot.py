import random
import board

from main import GameHandler
from board import GameBoard


class Bot:
    def __init__(self, color, depth=1):
        self.color = ''
        self.depth = depth
        if color == board.BLACK:
            self.color = 'black'
            self._opponent_color = board.WHITE
            self._color = board.BLACK
        elif color == board.WHITE:
            self._color = board.WHITE
            self._opponent_color = board.BLACK
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
        random_index = random.randint(0, len(possible_movies) - 1)
        move = possible_movies[random_index]
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        return 'OK', move


class MinMaxBot(Bot):

    def make_a_move(self):
        possible_movies = GameHandler.get_possible_movies()
        if len(possible_movies) == 0:
            _board = GameHandler.get_board()
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        if len(possible_movies) == 1:
            if self._color == board.WHITE:
                GameHandler.put_white(possible_movies[0])
            else:
                GameHandler.put_black(possible_movies[0])
            return 'OK', possible_movies[0]
        move = self.min_max(GameHandler.game_board, self.depth, self._color, self._opponent_color)[0]
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        # print(move)
        return 'OK', move

    def min_max(self, game_board: GameBoard, depth, current_color, next_color):
        if current_color == self._color:
            best_move = ['', -10000]
        else:
            best_move = ['', 10000]
        possible_next_movies_buff = game_board.possible_next_movies.copy()
        if len(possible_next_movies_buff) == 0:
            _board = game_board.board
            for square in _board:
                if _board[square] == 0:
                    possible_next_movies_buff.append(square)
        movies_value = {}
        for possible_move in possible_next_movies_buff:
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
            fake_game_board.possible_next_movies = possible_next_movies_buff.copy()
            fake_game_board.empty_squares = game_board.empty_squares
            fake_game_board.history_of_moves = game_board.history_of_moves[:]
            fake_game_board.next_color = game_board.next_color
            fake_game_board.put_piece(current_color, next_color, possible_move)
            movies_value[possible_move] = self.min_max(fake_game_board, depth - 1, next_color, current_color)[1]

        if len(movies_value) == 0:
            return best_move
        elif current_color == self._color:
            best_move = max(movies_value, key=movies_value.get)
        elif current_color == self._opponent_color:
            best_move = min(movies_value, key=movies_value.get)
        return [best_move, movies_value[best_move]]


class AlphaBetaBot(Bot):

    def __init__(self, color, depth=1):
        super().__init__(color, depth)
        self.alpha = -10000
        self.beta = 10000

    def make_a_move(self):
        self.alpha = -10000
        self.beta = 10000
        possible_movies = GameHandler.get_possible_movies()
        if len(possible_movies) == 0:
            _board = GameHandler.get_board()
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        if len(possible_movies) == 1:
            if self._color == board.WHITE:
                GameHandler.put_white(possible_movies[0])
            else:
                GameHandler.put_black(possible_movies[0])
            return 'OK', possible_movies[0]
        move = self.min_max(GameHandler.game_board, self.depth, self._color, self._opponent_color, -10000, 10000)[0]
        if self.color == 'white':
            GameHandler.put_white(move)
        elif self.color == 'black':
            GameHandler.put_black(move)
        print(move)
        return 'OK', move

    def min_max(self, game_board: GameBoard, depth, current_color, next_color, a, b):
        if current_color == self._color:
            best_move = ['', -10000]
        else:
            best_move = ['', 10000]
        possible_next_movies_buff = game_board.possible_next_movies.copy()
        if len(possible_next_movies_buff) == 0:
            _board = game_board.board
            for square in _board:
                if _board[square] == 0:
                    possible_next_movies_buff.append(square)
        movies_value = {}
        for possible_move in possible_next_movies_buff:
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
            fake_game_board.possible_next_movies = possible_next_movies_buff.copy()
            fake_game_board.empty_squares = game_board.empty_squares
            fake_game_board.history_of_moves = game_board.history_of_moves[:]
            fake_game_board.next_color = game_board.next_color
            fake_game_board.put_piece(current_color, next_color, possible_move)

            if current_color == self._color:
                # MAX
                a = self.min_max(fake_game_board, depth - 1, next_color, current_color, a, b)[1]
                movies_value[possible_move] = a
                if a >= b:
                    break

            else:
                # MIN
                b = self.min_max(fake_game_board, depth - 1, next_color, current_color, a, b)[1]
                movies_value[possible_move] = b
                if a >= b:
                    break

        if len(movies_value) == 0:
            return best_move
        elif current_color == self._color:
            best_move = max(movies_value, key=movies_value.get)

        elif current_color == self._opponent_color:
            best_move = min(movies_value, key=movies_value.get)

        return [best_move, movies_value[best_move]]
