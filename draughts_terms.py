from enum import Enum


class Color(Enum):
    WHITE = 1
    BLACK = 2


class GameState(Enum):
    WHITE_MOVE = Color.WHITE.value
    BLACK_MOVE = Color.BLACK.value
    WHITE_WON = 3
    BLACK_WON = 4
    DRAW = 5
