from server import DraughtsServer
from piece import Color
from clients.console_client import DraughtsConsoleClient


if __name__ == '__main__':
    server = DraughtsServer()
    white_player = DraughtsConsoleClient(Color.WHITE)
    black_player = DraughtsConsoleClient(Color.BLACK)

    while not server.game_over:
        if server.active_player_color == Color.WHITE:
            player = white_player
        else:
            player = black_player
        while True:
            try:
                x1, y1, x2, y2 = player.ask_for_move(server.board)
                server.move((x1, y1), (x2, y2))
                break
            except DraughtsServer.WrongMoveError as e:
                player.say('\033[93m' + e.message + '\033[0m')

    if server.winner == Color.WHITE:
        winner = white_player
        looser = black_player
    else:
        winner = black_player
        looser = white_player

    winner.say('Congratulations! You won!')
    looser.say('The game is over. You lost.')
