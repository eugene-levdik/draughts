from builtins import set

from draughts_terms import Color, GameState
from piece import Piece


class DraughtsBoard:
    """
    Stores all the information about Draughts game and processes moves.

    Creates a standard starting position when initialised.

    Attributes:
        state (GameState): Stores the state of the game (whose move it is or who won if the game has ended)
        pieces (list): Stores all the pieces that are on the bord
        __board__ (list): 8x8 2d array representing the game board
        __row_killer__ (Piece): Stores the piece that performs a row-kill. None while processing a non-row-kill
        __killed_in_row__ (list): List of pieces that have been killed in a row. Empty while processing a non-row-kill
    """

    class WrongMoveError(Exception):
        def __init__(self, message):
            self.message = message

    def __init__(self):
        self.state = GameState.WHITE_MOVE
        pieces = []

        # white
        for x in range(0, 8, 2):
            pieces.append(Piece(x, 0, Color.WHITE))
            pieces.append(Piece(x, 2, Color.WHITE))
        for x in range(1, 8, 2):
            pieces.append(Piece(x, 1, Color.WHITE))

        # black
        for x in range(0, 8, 2):
            pieces.append(Piece(x, 6, Color.BLACK))
        for x in range(1, 8, 2):
            pieces.append(Piece(x, 7, Color.BLACK))
            pieces.append(Piece(x, 5, Color.BLACK))

        self.pieces = pieces
        self.__board__ = None
        self.__update_board__()

        self.__row_killer__ = None
        self.__killed_in_row__ = []

    def __update_board__(self):
        """"
        Updates the 2d array representation of the board according to the list of pieces.
        Must be used each time a piece is moved or killed.
        """
        board = []
        for i in range(8):
            board.append([None] * 8)
        for piece in self.pieces:
            board[piece.x][piece.y] = piece
        self.__board__ = board

    def __can__kill__(self, killer, prey):
        """
        Checks if the killer piece can kill the pray piece considering the game state

        Args:
            killer (Piece): Piece that is going to kill
            prey (Piece): Piece to be killed

        Returns: bool
        """
        if self.__row_killer__ is not None and killer is not self.__row_killer__:
            return False
        if killer.color.value != self.state.value:
            return False
        if prey.color == killer.color:
            return False
        if abs(killer.x - prey.x) != abs(killer.y - prey.y):
            return False

        if killer.is_king:
            dx = 1 if prey.x > killer.x else -1
            dy = 1 if prey.y > killer.y else -1
            x, y = killer.x + dx, killer.y + dy
            while prey.x != x:
                for killed_piece in self.__killed_in_row__:
                    if x == killed_piece.x and y == killed_piece.y:
                        return False
                if self.__board__[x][y] is not None:
                    return False
                x += dx
                y += dy
            x_to = prey.x + dx
            y_to = prey.y + dy
        else:
            if abs(killer.x - prey.x) != 1:
                return False
            x_to = 2 * prey.x - killer.x
            y_to = 2 * prey.y - killer.y
        if not 0 <= x_to <= 7 or 0 <= y_to <= 7:
            return False
        if self.__board__[x_to][y_to] is not None:
            return False
        return True

    def __has_to_kill__(self):
        """
        Checks if the active player has to kill a piece

        Returns: bool
        """
        for killer in self.pieces:
            for prey in self.pieces:
                if self.__can__kill__(killer, prey):
                    return True
        return False

    def move(self, x1, y1, x2, y2):
        """"
        Processes a move and removes the killed piece off the board.
        Only one piece can be killed. If there is more to kill, the turn will not end (game state remains the same).

        Args:
            x1, y1 (integers from 0 to 7): Piece to move coordinates
            x2, y2 (integers from 0 to 7): Destination coordinates

        Raises:
              WrongMoveError: When the move is incorrect
        """

        for coordinate in (x1, x2, y1, y2):
            if coordinate > 7 or coordinate < 0:
                raise self.WrongMoveError('You are out of the board')
        piece_to_move = None
        for piece in self.pieces:
            if piece.x == x2 and piece.y == y2:
                raise self.WrongMoveError('You can not move here')
            if piece.x == x1 and piece.y == y1:
                piece_to_move = piece
        if piece_to_move is None:
            raise self.WrongMoveError('You did not select any piece')
        if piece_to_move.color.value != self.state.value:
            raise self.WrongMoveError('You can not move the opponent\'s pieces')
        if self.__row_killer__ is not None and piece_to_move is not self.__row_killer__:
            raise self.WrongMoveError('Yoy can not move this piece')
        if abs(x2 - x1) != abs(y2 - y1):
            raise self.WrongMoveError('You can not move here')

        piece_to_kill = None
        if piece_to_move.is_king:
            dx = -1 if x2 > x1 else 1
            dy = -1 if y2 > y1 else 1
            x, y = x2 - dx, y2 - dy
            while True:
                if self.__board__[x][y] is not None:
                    x += dx
                    y += dy
                    continue
                if x == x1:
                    break
                piece_to_kill = self.__board__[x][y]
                if not self.__can__kill__(piece_to_move, piece_to_kill):
                    raise self.WrongMoveError('You can not move here')
                break
        else:
            if not 1 <= abs(x2 - x1) <= 2:
                raise self.WrongMoveError('You can not move here')
            if abs(x2 - x1) == 2:
                mid_x = int((x1 + x2) / 2)
                mid_y = int((y1 + y2) / 2)
                piece_to_kill = self.__board__[mid_x][mid_y]
                if piece_to_kill is None:
                    raise self.WrongMoveError('You can not move here')
                if piece_to_kill.color == piece_to_move.color:
                    raise self.WrongMoveError('You can not move here')

        if self.__has_to_kill__():
            if piece_to_kill is None:
                raise self.WrongMoveError('There are pieces you must kill')
            piece_to_move.move(x2, y2)
            self.pieces.remove(piece_to_kill)
            self.__update_board__()
            if not self.__has_to_kill__():
                self.__row_killer__ = None
                self.__killed_in_row__ = []
            else:
                self.__row_killer__ = piece_to_move
                self.__killed_in_row__.append(piece_to_kill)
                self.state = GameState.WHITE_MOVE if self.state == GameState.BLACK_MOVE else GameState.BLACK_MOVE
        else:
            piece_to_move.move(x2, y2)
            self.__update_board__()
            self.state = GameState.WHITE_MOVE if self.state == GameState.BLACK_MOVE else GameState.BLACK_MOVE

        white_count = 0
        black_count = 0
        for piece in self.pieces:
            if piece.color == Color.WHITE:
                white_count += 1
                if piece.y == 7:
                    piece.is_king = True
            else:
                black_count += 1
                if piece.y == 0:
                    piece.is_king = True
        if white_count == 0:
            self.state = GameState.BLACK_WON
        elif black_count == 0:
            self.state = GameState.WHITE_WON


if __name__ == '__main__':
    server = DraughtsBoard()
    print(server.state)
    server.move(0, 2, 1, 3)
    print(server.state)
    for y in range(8):
        for x in range(8):
            piece = server.__board__[x][y]
            if piece is None:
                piece = '■' if (x + y) % 2 == 1 else '□'
            print(piece, end='', sep='')
        print()
    # try:
    #     server.move(0, 4, 1, 4)
    # except DraughtsBoard.WrongMoveError as e:
    #     print('\033[93m' + e.message + '\033[0m')
