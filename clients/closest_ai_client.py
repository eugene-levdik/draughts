from clients.draughts_client import DraughtsClient
import random as r
from piece import Color


def gen_x():
    return r.randint(0, 7)


def gen_y(color):
    y = 8
    while y > 7:
        y = int(abs(r.gauss(0, 4)))
    if color == Color.BLACK:
        y = 7 - y
    return y


class ClosestDraughtsClient(DraughtsClient):

    def ask_for_move(self, board):
        return gen_x(), gen_y(self.color), gen_x(), gen_y(self.color)
