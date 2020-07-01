from enum import Enum


class Color(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


class Piece:

    def __init__(self, color):
        self.color = color
        self.is_king = False
        self.killed = False

    def __repr__(self):
        if self.color == Color.WHITE:
            return '\033[94m⛁\033[0m' if self.is_king else '\033[94m⛀\033[0m'
        if self.color == Color.BLACK:
            return '\033[91m⛃\033[0m' if self.is_king else '\033[91m⛂\033[0m'
        return ''
