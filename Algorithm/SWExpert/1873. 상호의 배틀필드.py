for t in range(int(input())):
    h, w = map(int, input().split())
    board = []
    for _ in range(h):
        board.append(list(map(str, input())))
    n = int(input())
    s = input()
    print('#' + str(t+1), end=' ')
    x, y = 0, 0
    for i in range(h):
        for j in range(w):
            if board[i][j] in '^v<>':
                x, y = j, i
                break
    for c in s:
        if c == 'U':
            board[y][x] = '^'
            if y-1 >= 0:
                if board[y-1][x] == '.':
                    board[y][x], board[y-1][x] = '.', '^'
                    y -= 1
        elif c =='D':
            board[y][x] = 'v'
            if y+1 < h:
                if board[y+1][x] == '.':
                    board[y][x], board[y+1][x] = '.', 'v'
                    y += 1
        elif c == 'L':
            board[y][x] = '<'
            if x-1 >= 0:
                if board[y][x-1] == '.':
                    board[y][x], board[y][x-1] = '.', '<'
                    x -= 1
        elif c == 'R':
            board[y][x] = '>'
            if x+1 < w:
                if board[y][x+1] == '.':
                    board[y][x], board[y][x+1] = '.', '>'
                    x += 1
        else:
            if board[y][x] == '^':
                for i in range(y-1, -1, -1):
                    if board[i][x] == '#':
                        break
                    elif board[i][x] == '*':
                        board[i][x] = '.'
                        break
            elif board[y][x] == 'v':
                for i in range(y+1, h):
                    if board[i][x] == '#':
                        break
                    elif board[i][x] == '*':
                        board[i][x] ='.'
                        break
            elif board[y][x] == '<':
                for i in range(x-1, -1, -1):
                    if board[y][i] == '#':
                        break
                    elif board[y][i] == '*':
                        board[y][i] = '.'
                        break
            else:
                for i in range(x+1, w):
                    if board[y][i] == '#':
                        break
                    elif board[y][i] == '*':
                        board[y][i] = '.'
                        break
    for i in range(h):
        for j in range(w):
            print(board[i][j], end='')
        print()