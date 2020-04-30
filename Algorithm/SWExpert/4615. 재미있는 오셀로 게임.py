for t in range(int(input())):
    n, m = map(int, input().split())
    board = [[0]*n for _ in range(n)]
    board[(n//2)-1][(n//2)-1], board[(n//2)-1][n//2], board[n//2][(n//2)-1], board[n//2][n//2] = 2, 1, 1, 2
    direction = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]]
    answer = [0]*2
    for _ in range(m):
        x, y, c = map(int, input().split())
        x, y = x-1, y-1
        board[y][x] = c
        for l in direction:
            move_x, move_y = x+l[0], y+l[1]
            confirm = False
            while move_x >= 0 and move_x < n and move_y >= 0 and move_y < n:
                if board[move_y][move_x] == 0:
                    break
                elif board[y][x] != board[move_y][move_x]:
                    move_x += l[0]
                    move_y += l[1]
                    confirm = True
                elif confirm and board[y][x] == board[move_y][move_x]:
                    if l[0] == 0 and l[1] == 1:
                        for i in range(y+1, move_y):
                            board[i][x] = c
                    elif l[0] == 0 and l[1] == -1:
                        for i in range(move_y+1, y):
                            board[i][x] = c
                    elif l[0] == 1 and l[1] == 0:
                        for i in range(x+1, move_x):
                            board[y][i] = c
                    elif l[0] == -1 and l[1] == 0:
                        for i in range(move_x+1, x):
                            board[y][i] = c
                    else:
                        for i in range(1, abs(move_y-y)):
                            board[y+(i*l[1])][x+(i*l[0])] = c
                    break
                else:
                    break
    for i in range(n):
        for j in range(n):
            if board[i][j] == 1:
                answer[0] += 1
            elif board[i][j] == 2:
                answer[1] += 1
    print('#' + str(t+1) + ' ' + str(answer[0]) + ' ' + str(answer[1]))