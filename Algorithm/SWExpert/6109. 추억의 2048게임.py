for t in range(int(input())):
    n, direction = map(str, input().split())
    board = []
    for _ in range(int(n)):
        board.append(list(map(int, input().split())))
    if direction == 'up':
        for w in range(len(board[0])):
            change = []
            for h in range(1, len(board)):
                if board[h][w] != 0:
                    for i in range(h-1, -1, -1):
                        if board[i][w] == 0:
                            board[i][w] = board[i+1][w]
                            board[i+1][w] = 0
                        else:
                            if board[i][w] == board[i+1][w] and i not in change:
                                board[i][w] *= 2
                                board[i+1][w] = 0
                                change.append(i)
                            break
    elif direction == 'down':
        for w in range(len(board[0])):
            change = []
            for h in range(len(board)-2, -1, -1):
                if board[h][w] != 0:
                    for i in range(h+1, len(board)):
                        if board[i][w] == 0:
                            board[i][w] = board[i-1][w]
                            board[i-1][w] = 0
                        else:
                            if board[i][w] == board[i-1][w] and i not in change:
                                board[i][w] *= 2
                                board[i-1][w] = 0
                                change.append(i)
                            break
    elif direction == 'left':
        for h in range(len(board)):
            change = []
            for w in range(1, len(board[0])):
                if board[h][w] != 0:
                    for i in range(w-1, -1, -1):
                        if board[h][i] == 0:
                            board[h][i] = board[h][i+1]
                            board[h][i+1] = 0
                        else:
                            if board[h][i] == board[h][i+1] and i not in change:
                                board[h][i] *= 2
                                board[h][i+1] = 0
                                change.append(i)
                            break
    else:
        for h in range(len(board)):
            change = []
            for w in range(len(board[0])-2, -1, -1):
                if board[h][w] != 0:
                    for i in range(w+1, len(board[0])):
                        if board[h][i] == 0:
                            board[h][i] = board[h][i-1]
                            board[h][i-1] = 0
                        else:
                            if board[h][i] == board[h][i-1] and i not in change:
                                board[h][i] *= 2
                                board[h][i-1] = 0
                                change.append(i)
                            break
    print('#' + str(t+1))
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[i][j], end=' ')
        print()