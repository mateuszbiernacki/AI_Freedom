import requests
import random

import board


class Bot:
    def __init__(self, color):
        self.color = ''
        if color == board.BLACK:
            self.color = 'black'
        elif color == board.WHITE:
            self.color = 'white'

    def make_a_move(self, possible_movies, board):
        pass


class RandomBot(Bot):
    def make_a_move(self, possible_movies, board):
        random_index = random.randint(0, len(possible_movies)-1)
        response = requests.get(f'http://127.0.0.1:5000/put/{self.color}/{possible_movies[random_index]}')

