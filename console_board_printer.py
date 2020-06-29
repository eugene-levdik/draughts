from piece import Color


def print_to_console(view, board):
    board_to_print = []
    for i in range(8):
        line = []
        for j in range(8):
            line.append('■' if (i + j) % 2 == 0 else '□')
        board_to_print.append(line)
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece.color == Color.EMPTY or piece.killed:
                continue
            board_to_print[x][y] = piece.__repr__()

    if view == Color.WHITE:
        for y in range(8):
            print(8 - y, sep='', end=' ')
            for x in range(8):
                print(board_to_print[x][7 - y], sep='', end=' ')
            print()
        print('  A  B C  D  E F  G H')
        # print('  A B  C D  E F  G H')
    else:
        for y in range(8):
            print(y + 1, sep='', end=' ')
            for x in range(8):
                print(board_to_print[7 - x][y], sep='', end=' ')
            print()
        print('  H  G F  E  D C  B A')
        # print('  H G  F E  D C  B A')
