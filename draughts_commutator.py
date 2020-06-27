from draughts_server import DraughtsBoard
from console_client import DraughtsConsoleClient
from draughts_terms import Color, GameState


if __name__ == '__main__':
    server = DraughtsBoard()
    white_player = DraughtsConsoleClient(Color.WHITE)
    black_player = DraughtsConsoleClient(Color.BLACK)

    while True:
        if server.state == GameState.WHITE_MOVE:
            player = white_player
        elif server.state == GameState.BLACK_MOVE:
            player = black_player
        else:
            break
        while True:
            try:
                x1, y1, x2, y2 = player.ask_for_move(server.pieces)
                server.move(x1, y1, x2, y2)
                break
            except DraughtsBoard.WrongMoveError as e:
                player.say('\033[93m' + e.message + '\033[0m')

    if server.state == GameState.DRAW:
        white_player.say('The game ended in a draw.')
        exit()

    if server.state == GameState.WHITE_WON:
        winner = white_player
        looser = black_player
    else:
        winner = black_player
        looser = white_player

    winner.say('Congratulations! You won!')
    looser.say('The game is over. You lost.')
