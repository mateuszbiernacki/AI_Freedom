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

SQUARES_CORD = {}
for i in range(len(SQUARES_NAMES)):
    for j in range(len(SQUARES_NAMES[i])):
        SQUARES_CORD[SQUARES_NAMES[i][j]] = (j, i)


class GameBoard:
    def __init__(self):
        self.board = {}
        self.empty_squares = 100
        self.last_move = []
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
                    # print(x, y)
                    if x in range(1, 11) and y in range(1, 11):
                        if self.board[SQUARES_NAMES[y - 1][x - 1]] == EMPTY:
                            self.possible_next_movies.append(SQUARES_NAMES[y - 1][x - 1])
            if color == BLACK:
                self.last_move = [square_name, 'black']
            elif color == WHITE:
                self.last_move = [square_name, 'white']
            self.history_of_moves += square_name + ' '
            return 'OK'
        else:
            return 'E1'

    def count_current_result(self, color):
        # Every square is counted in 4 ways: across, down and crosswise two times (| -- / \)
        points = 0
        for square in self.board:
            if self.board[square] == color:
                x = -1
                for iterator in range(10):
                    if square[0] == LETTERS[iterator]:
                        y = iterator
                x = int(square[1:])-1
                # across
                in_one_line = 1
                x_iter, y_iter = x+1, y  # x+1 because there is checked square in right side
                while x_iter < 10 and y_iter < 10:
                    # Reject when it is consecutive this color square
                    if 0 <= x - 1 < 10 and 0 <= y < 10:
                        if self.board[SQUARES_NAMES[y][x - 1]] == color:
                            break
                    if self.board[SQUARES_NAMES[y_iter][x_iter]] == color:
                        in_one_line += 1
                        x_iter += 1
                    else:
                        break
                if in_one_line == 4:
                    print(square, '->', SQUARES_NAMES[y_iter][x_iter-1])
                    points += 1

                # down
                in_one_line = 1
                x_iter, y_iter = x, y+1  # y+1 because there is checked square in down side
                while x_iter < 10 and y_iter < 10:
                    # Reject when it is consecutive this color square
                    if 0 <= x < 10 and 0 <= y - 1 < 10:
                        if self.board[SQUARES_NAMES[y-1][x]] == color:
                            break
                    if self.board[SQUARES_NAMES[y_iter][x_iter]] == color:
                        in_one_line += 1
                        y_iter += 1
                    else:
                        break
                if in_one_line == 4:
                    print(square, '->', SQUARES_NAMES[y_iter-1][x_iter])
                    points += 1

                # crosswise \
                in_one_line = 1
                x_iter, y_iter = x+1, y+1  # y+1 and x+1 because there is checked square in right-down side
                while x_iter < 10 and y_iter < 10:
                    # Reject when it is consecutive this color square
                    if 0 <= x - 1 < 10 and 0 <= y - 1 < 10:
                        if self.board[SQUARES_NAMES[y-1][x-1]] == color:
                            break
                    if self.board[SQUARES_NAMES[y_iter][x_iter]] == color:
                        in_one_line += 1
                        y_iter += 1
                        x_iter += 1
                    else:
                        break
                if in_one_line == 4:
                    print(square, '->', SQUARES_NAMES[y_iter-1][x_iter-1])
                    points += 1

                # crosswise /
                in_one_line = 1
                x_iter, y_iter = x - 1, y + 1  # y+1 and x-1 because there is checked square in left-down side
                while 0 <= x_iter < 10 and y_iter < 10:
                    # Reject when it is consecutive this color square
                    if 0 <= x + 1 < 10 and 0 <= y - 1 < 10:
                        if self.board[SQUARES_NAMES[y - 1][x + 1]] == color:
                            break
                    if self.board[SQUARES_NAMES[y_iter][x_iter]] == color:
                        in_one_line += 1
                        y_iter += 1
                        x_iter -= 1
                    else:
                        break
                if in_one_line == 4:
                    print(square, '->', SQUARES_NAMES[y_iter - 1][x_iter + 1])
                    points += 1

        return str(points)

    def reset(self):
        for square in self.board:
            self.board[square] = EMPTY


class GameHandler:
    game_board = GameBoard()

    @staticmethod
    def put_white(square_name):
        return GameHandler.game_board.put_piece(WHITE, BLACK, square_name)

    @staticmethod
    def put_black(square_name):
        return GameHandler.game_board.put_piece(BLACK, WHITE, square_name)

    @staticmethod
    def get_board():
        return GameHandler.game_board.board

    @staticmethod
    def get_possible_movies():
        return GameHandler.game_board.possible_next_movies

    @staticmethod
    def get_black_points():
        return GameHandler.game_board.count_current_result(BLACK)

    @staticmethod
    def get_white_points():
        return GameHandler.game_board.count_current_result(WHITE)


