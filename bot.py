import requests
import random
import json
import board


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
        possible_movies = json.loads(requests.get('http://127.0.0.1:5000/possible_movies').text.encode('utf-8'))
        if len(possible_movies) == 0:
            _board = json.loads(requests.get('http://127.0.0.1:5000/board').text.encode('utf-8'))
            for square in _board:
                if _board[square] == 0:
                    possible_movies.append(square)
        random_index = random.randint(0, len(possible_movies)-1)
        move = possible_movies[random_index]
        # print(possible_movies)
        response = requests.get(f'http://127.0.0.1:5000/put/{self.color}/{move}')
        return response.text, move

