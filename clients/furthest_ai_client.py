from clients.draughts_client import DraughtsAIClient
import random as r
from piece import Color


def gen_x():
    return r.randint(0, 7)


def gen_y(color):
    y = 8
    while y > 7:
        y = int(abs(r.gauss(0, 4)))
    if color == Color.WHITE:
        y = 7 - y
    return y


class FurthestDraughtsClient(DraughtsAIClient):

    def ask_for_move(self, board, color):
        return gen_x(), gen_y(color), gen_x(), gen_y(color)

    def __repr__(self):
        return 'Furthest AI'
