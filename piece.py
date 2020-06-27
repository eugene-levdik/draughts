from draughts_terms import Color


class Piece:

    def __init__(self, x, y, color):
        self.is_king = False
        self.x, self.y = x, y
        self.color = color

    def move(self, x, y):
        self.x, self.y = x, y
        if self.color == Color.WHITE and y == 7:
            self.is_king = True
        if self.color == Color.BLACK and y == 0:
            self.is_king = True

    def __repr__(self):
        if self.color == Color.WHITE:
            return '⛁' if self.is_king else '⛀'
        return '⛃' if self.is_king else '⛂'


if __name__ == '__main__':
    piece = Piece(0, 0, Color.WHITE)
    print(piece)
    piece.move(1, 7)
    print(piece)
