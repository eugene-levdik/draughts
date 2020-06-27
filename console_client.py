from draughts_client import DraughtsClient
from draughts_terms import Color
# from draughts_server import DraughtsBoard


class DraughtsConsoleClient(DraughtsClient):

    def ask_for_move(self, pieces):
        board = []
        for i in range(8):
            line = []
            for j in range(8):
                line.append('□' if (i + j) % 2 == 0 else '■')
            board.append(line)
        for piece in pieces:
            board[piece.x][piece.y] = piece.__repr__()

        print('Player ' + str(self.color.value) + ', what is your move?')
        if self.color == Color.WHITE:
            for y in range(8):
                print(8 - y, sep='', end=' ')
                for x in range(8):
                    print(board[x][7 - y], sep='', end=' ')
                print()
            print('  A  B C  D  E F  G H')
        else:
            for y in range(8):
                print(y + 1, sep='', end=' ')
                for x in range(8):
                    print(board[7 - x][y], sep='', end=' ')
                print()
            print('  H  G F  E  D C  B A')

        while True:
            try:
                print('From: ', end='')
                from_coordinates = input().lower()
                print('To: ', end='')
                to_coordinates = input().lower()
                x1 = ord(from_coordinates[0]) - ord('a')
                y1 = int(from_coordinates[1]) - 1
                x2 = ord(to_coordinates[0]) - ord('a')
                y2 = int(to_coordinates[1]) - 1
                return x1, y1, x2, y2
            except Exception:
                print('Incorrect input. Please, use \'e2 e4\' notation')

    def say(self, message):
        print(message)


# if __name__ == '__main__':
#     client = DraughtsConsoleClient(Color.BLACK)
#     server = DraughtsBoard()
#     client.ask_for_move(server.pieces)
