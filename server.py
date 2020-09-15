from builtins import range
from piece import Color, Piece


class DraughtsServer:

    class WrongMoveError(Exception):
        def __init__(self, message=None):
            if message is None:
                self.message = 'You can not move here'
            else:
                self.message = message

    def __init__(self):
        self.game_over = False
        self.active_player_color = Color.WHITE
        self.winner = None

        self.board = []
        for i in range(8):
            self.board.append([Piece(Color.EMPTY)] * 8)
        for x in range(0, 8, 2):
            self.board[x][0] = Piece(Color.WHITE)
            self.board[x + 1][1] = Piece(Color.WHITE)
            self.board[x][2] = Piece(Color.WHITE)
        for x in range(0, 8, 2):
            self.board[x + 1][5] = Piece(Color.BLACK)
            self.board[x][6] = Piece(Color.BLACK)
            self.board[x + 1][7] = Piece(Color.BLACK)

        self.__row_killer_pos__ = None

    def __find_inbetween__(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        inbetween = []
        if abs(x2 - x1) != abs(y2 - y1):
            return inbetween
        if x1 == x2:
            return inbetween
        dx = 1 if x2 > x1 else -1
        dy = 1 if y2 > y1 else -1
        x = x1 + dx
        y = y1 + dy
        while x != x2:
            piece = self.board[x][y]
            if piece.color != Color.EMPTY:
                inbetween.append((x, y))
            x += dx
            y += dy
        return inbetween

    def __piece_can_kill__(self, pos):
        x, y = pos
        piece = self.board[x][y]

        if self.__row_killer_pos__ is not None and pos != self.__row_killer_pos__:
            return False
        if piece.color != self.active_player_color:
            return False

        for dx in (1, -1):
            for dy in (1, -1):
                x_check = x + dx
                y_check = y + dy
                if piece.is_king:
                    while 0 < x_check < 7 and 0 < y_check < 7:
                        piece_to_kill = self.board[x_check][y_check]
                        if piece_to_kill.color == Color.EMPTY:
                            x_check += dx
                            y_check += dy
                            continue
                        if piece_to_kill.color == piece.color or piece_to_kill.killed:
                            break
                        if not self.board[x_check + dx][y_check + dy].color == Color.EMPTY:
                            break
                        return True
                else:
                    if x_check <= 0 or x_check >= 7 or y_check <= 0 or y_check >= 7:
                        continue
                    piece_to_kill = self.board[x_check][y_check]
                    if piece_to_kill.color == Color.EMPTY:
                        continue
                    if piece_to_kill.color == piece.color or piece_to_kill.killed:
                        continue
                    if not self.board[x_check + dx][y_check + dy].color == Color.EMPTY:
                        continue
                    return True
        return False

    def __has_to_kill__(self):
        for x in range(8):
            for y in range(8):
                if self.__piece_can_kill__((x, y)):
                    return True
        return False

    def __pass_turn__(self):
        for x in range(8):
            for y in range(8):
                if self.board[x][y].killed:
                    self.board[x][y] = Piece(Color.EMPTY)
        self.__row_killer_pos__ = None
        if self.active_player_color == Color.WHITE:
            self.active_player_color = Color.BLACK
        else:
            self.active_player_color = Color.WHITE

    def __check_winner__(self):
        white_counter = 0
        black_counter = 0
        for x in range(8):
            for y in range(8):
                piece = self.board[x][y]
                if piece.color == Color.EMPTY or piece.killed:
                    continue
                if piece.color == Color.WHITE:
                    white_counter += 1
                else:
                    black_counter += 1
        if white_counter == 0:
            return Color.BLACK
        if black_counter == 0:
            return Color.WHITE
        return None

    def move(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        for coordinate in (x1, x2, y1, y2):
            if coordinate > 7 or coordinate < 0:
                raise self.WrongMoveError(message='You are out of the board')
        piece_to_move = self.board[x1][y1]
        if piece_to_move.color == Color.EMPTY:
            raise self.WrongMoveError(message='You did not select any piece')
        if piece_to_move.color != self.active_player_color:
            raise self.WrongMoveError(message='You can not move the opponent\'s pieces')
        if self.board[x2][y2].color != Color.EMPTY:
            raise self.WrongMoveError()
        if abs(x2 - x1) != abs(y2 - y1):
            raise self.WrongMoveError()

        inbetween = self.__find_inbetween__(pos1, pos2)
        if self.__row_killer_pos__ is None:
            if len(inbetween) > 1:
                raise self.WrongMoveError()
            if len(inbetween) == 0:
                if self.__has_to_kill__():
                    raise self.WrongMoveError('There is a piece to kill')
                if not piece_to_move.is_king and y2 - y1 != (1 if piece_to_move.color == Color.WHITE else -1):
                    raise self.WrongMoveError()
                self.board[x2][y2] = piece_to_move
                self.board[x1][y1] = Piece(Color.EMPTY)
                self.__pass_turn__()
                if piece_to_move.color == Color.WHITE and y2 == 7:
                    piece_to_move.is_king = True
                if piece_to_move.color == Color.BLACK and y2 == 0:
                    piece_to_move.is_king = True
                return
        else:
            if self.__row_killer_pos__ != pos1:
                raise self.WrongMoveError(message='You have to continue with the piece you have already moved')
            if len(inbetween) != 1:
                raise self.WrongMoveError()

        x_kill, y_kill = inbetween[0]
        piece_to_kill = self.board[x_kill][y_kill]
        if piece_to_move.color == piece_to_kill.color or piece_to_kill.killed:
            raise self.WrongMoveError()
        if not piece_to_move.is_king and abs(x2 - x1) != 2:
            raise self.WrongMoveError()
        piece_to_kill.killed = True
        self.board[x1][y1] = Piece(Color.EMPTY)
        self.board[x2][y2] = piece_to_move

        if piece_to_move.color == Color.WHITE and y2 == 7:
            piece_to_move.is_king = True
        if piece_to_move.color == Color.BLACK and y2 == 0:
            piece_to_move.is_king = True

        self.winner = self.__check_winner__()
        if self.winner is not None:
            self.game_over = True
            self.active_player_color = None
            return

        self.__row_killer_pos__ = pos2
        if not self.__has_to_kill__():
            self.__pass_turn__()
