import json
from threading import Thread
from flask import Flask

flask_app = Flask('__name__')


class GameHandler(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        flask_app.run()


@flask_app.route('/')
def test():
    return 'test'


if __name__ == '__main__':
    game_handler = GameHandler()
    game_handler.start()
