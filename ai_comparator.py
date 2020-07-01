from server import DraughtsServer
from piece import Color
from clients.furthest_ai_client import FurthestDraughtsClient
import time
from clients.closest_ai_client import ClosestDraughtsClient


if __name__ == '__main__':
    closest = ClosestDraughtsClient()
    furthest = FurthestDraughtsClient()
    n = 100
    for i in range(n):
        print(round(100 * i / n), '%')
        server = DraughtsServer()
        moves = 0
        start = time.time()
        if i % 2 == 0:
            white_player = closest
            black_player = furthest
        else:
            white_player = furthest
            black_player = closest
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
                    x1, y1, x2, y2 = player.ask_for_move(server.board, server.active_player_color)
                    server.move((x1, y1), (x2, y2))
                    break
                except DraughtsServer.WrongMoveError:
                    pass
            moves += 1
            if moves > 100:
                print('Interrupting game while', player, 'move')
                break

        if server.winner == Color.WHITE:
            white_player.wins += 1
        elif server.winner == Color.BLACK:
            black_player.wins += 1

    print(closest, 'won', closest.wins, 'games')
    print(furthest, 'won', furthest.wins, 'games')
