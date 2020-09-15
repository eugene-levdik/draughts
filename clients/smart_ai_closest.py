from clients.draughts_client import DraughtsClient
import random as r
from piece import Color


regular_moves = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
kill_moves = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
king_moves = [(d, d) for d in range(1, 8)] + \
             [(d, -d) for d in range(1, 8)] + \
             [(-d, d) for d in range(1, 8)] + \
             [(-d, -d) for d in range(1, 8)]


class ClosestSmartClient(DraughtsClient):

    def ask_for_move(self, board):
        my_pieces = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j].color == self.color:
                    my_pieces.append((i, j))
        my_pieces.sort(key=lambda x: x[1])
        index = int(abs(r.gauss(0, len(my_pieces)) % len(my_pieces)))
        if self.color == Color.BLACK:
            index = len(my_pieces) - 1 - index
        x_from, y_from = my_pieces[index]
        if board[x_from][y_from].is_king:
            dx, dy = r.choice(king_moves)
            return x_from, y_from, x_from + dx, y_from + dy
        dx, dy = r.choice(regular_moves + kill_moves)
        return x_from, y_from, x_from + dx, y_from + dy

    def is_human(self):
        return False
