def solution(m, n, board2):
    answer = 0
    board = list()
    for i in range(m):
        board.append([])
        for j in range(n):
            board[-1].append(board2[i][j])
    while True:
        remove = False
        delete = list()
        for i in range(m-1):
            for j in range(n-1):
                if len(set(board[i][j] + board[i][j+1] + board[i+1][j] + board[i+1][j+1])) == 1 \
                    and list(set(board[i][j] + board[i][j+1] + board[i+1][j] + board[i+1][j+1]))[0] != ' ':
                        delete.append([i, j])
                        remove = True
        if remove:
            for i in range(len(delete)):
                board[delete[i][0]][delete[i][1]] = ' '
                board[delete[i][0]][delete[i][1] + 1] = ' '
                board[delete[i][0] + 1][delete[i][1]] = ' '
                board[delete[i][0] + 1][delete[i][1] + 1] = ' '
            for i in range(m-1, 0, -1):
                for j in range(n):
                    if board[i][j] == ' ':
                        for k in range(i-1, -1, -1):
                            if board[k][j] !=  ' ':
                                board[i][j] = board[k][j]
                                board[k][j] = ' '
                                break
        else:
            break
    for i in range(m):
        for j in range(n):
            if board[i][j] == ' ':
                answer += 1
    return answer