import requests
import flask
import json

flask_app = flask.Flask('__name__')

SQUARES_NAMES = (
    ('A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'),
    ('B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10'),
    ('C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'),
    ('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10'),
    ('E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10'),
    ('F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10'),
    ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10'),
    ('H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10'),
    ('I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7', 'I8', 'I9', 'I10'),
    ('J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'J9', 'J10'),
)
EMPTY = 0
BLACK = 1
WHITE = 2

LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']


def put_white_pawn(square_name):
    response = requests.get(f'http://127.0.0.1:5000/put/white/{square_name}')
    return response.text


def put_black_pawn(square_name):
    response = requests.get(f'http://127.0.0.1:5000/put/black/{square_name}')
    return response.text


class GameBoard:
    def __init__(self):
        self.board = {}
        self.empty_squares = 100
        self.history_of_moves = ''
        self.next_color = WHITE
        self.possible_next_movies = []
        for y in range(10):
            for x in range(10):
                self.board[SQUARES_NAMES[y][x]] = EMPTY
                self.possible_next_movies.append(SQUARES_NAMES[y][x])
        # for i in self.board:
        #     print(i)

    def is_it_possible_move(self, color, square):
        # Is it this color turn?
        if self.next_color == color:
            # Is square empty?
            if self.board[square] == EMPTY:
                # Is it possible move?
                if square in self.possible_next_movies:
                    return True
                else:
                    # Is it freedom?
                    if len(self.possible_next_movies) == 0:
                        return True
                    else:
                        return False
            else:
                return False
        else:
            return False

    def put_piece(self, color, next_color, square_name):
        if self.is_it_possible_move(color, square_name):
            self.board[square_name] = color
            self.next_color = next_color
            self.possible_next_movies = []
            y = square_name[0]
            y_val = -1
            for iter_letters in range(len(LETTERS)):
                if LETTERS[iter_letters] == y:
                    y_val = iter_letters + 1
                    break
            x_val = int(square_name[1:])
            for x in range(x_val - 1, x_val - 1 + 3):
                for y in range(y_val - 1, y_val - 1 + 3):
                    print(x, y)
                    if x in range(1, 11) and y in range(1, 11):
                        if self.board[SQUARES_NAMES[y - 1][x - 1]] == EMPTY:
                            self.possible_next_movies.append(SQUARES_NAMES[y - 1][x - 1])
            return 'OK'
        else:
            return 'E1'


game_board = GameBoard()


@flask_app.route('/')
def test():
    return 'test'


@flask_app.route('/put/white/<square_name>')
def put_white(square_name):
    return game_board.put_piece(WHITE, BLACK, square_name)


@flask_app.route('/put/black/<square_name>')
def put_black(square_name):
    return game_board.put_piece(BLACK, WHITE, square_name)


@flask_app.route('/board')
def get_board():
    return json.dumps(game_board.board)


if __name__ == '__main__':
    flask_app.run()
