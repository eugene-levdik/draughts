from clients.draughts_client import DraughtsClient
from console_board_printer import print_to_console


class DraughtsConsoleClient(DraughtsClient):

    def ask_for_move(self, board):
        print('Player ' + str(self.color.value) + ', what is your move?')

        print_to_console(self.color, board)

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
