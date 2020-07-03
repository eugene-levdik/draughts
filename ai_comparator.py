from server import DraughtsServer
from piece import Color
from clients.furthest_ai_client import FurthestDraughtsClient
from clients.closest_ai_client import ClosestDraughtsClient
import time


if __name__ == '__main__':
    closest_wins = 0
    furthest_wins = 0
    n = 100
    for i in range(n):
        print(round(100 * i / n), '%')
        server = DraughtsServer()
        moves = 0
        start = time.time()
        if i % 2 == 0:
            white_player = ClosestDraughtsClient(Color.WHITE)
            black_player = FurthestDraughtsClient(Color.BLACK)
        else:
            white_player = FurthestDraughtsClient(Color.WHITE)
            black_player = ClosestDraughtsClient(Color.BLACK)
        while not server.game_over:
            if server.active_player_color == Color.WHITE:
                player = white_player
            else:
                player = black_player
            while True:
                if time.time() - start > 10:
                    moves = 1e6
                    break
                try:
                    x1, y1, x2, y2 = player.ask_for_move(server.board)
                    server.move((x1, y1), (x2, y2))
                    break
                except DraughtsServer.WrongMoveError:
                    pass
            moves += 1
            if moves > 100:
                print('Interrupting game while', player, 'move')
                break

        if (i % 2 == 0 and server.winner == Color.WHITE) or (i % 2 == 1 and server.winner == Color.BLACK):
            closest_wins += 1
        elif (i % 2 == 1 and server.winner == Color.WHITE) or (i % 2 == 0 and server.winner == Color.BLACK):
            furthest_wins += 1

    print('Closest AI won', closest_wins, 'games')
    print('Furthest AI won', furthest_wins, 'games')
