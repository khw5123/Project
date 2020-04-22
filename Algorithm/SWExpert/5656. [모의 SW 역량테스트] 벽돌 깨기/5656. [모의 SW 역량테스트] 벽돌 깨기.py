import copy

def boom(n, w, h, board, destroy):
    while len(destroy) != 0:
        x, y, num = destroy[0][0], destroy[0][1], destroy[0][2]
        board[y][x] = 0
        for i in range(1, num):
            if x+i < w:
                if board[y][x+i] != 0:
                    destroy.append([x+i, y, board[y][x+i]])
            else:
                break
        for i in range(1, num):
            if x-i >= 0:
                if board[y][x-i] != 0:
                    destroy.append([x-i, y, board[y][x-i]])
            else:
                break
        for i in range(1, num):
            if y+i < h:
                if board[y+i][x] != 0:
                    destroy.append([x, y+i, board[y+i][x]])
            else:
                break
        for i in range(1, num):
            if y-i >= 0:
                if board[y-i][x] != 0 :
                    destroy.append([x, y-i, board[y-i][x]])
            else:
                break
        del destroy[0]
    for i in range(h-1, -1, -1):
        for j in range(w):
            if board[i][j] != 0:
                for k in range(i+1, h):
                    if board[k][j] == 0:
                        board[k][j] = board[k-1][j]
                        board[k-1][j] = 0
                    else:
                        break

def solve(n, w, h, board, answer):
    if n == 0:
        tmp = 0
        for i in range(h):
            for j in range(w):
                if board[i][j] != 0:
                    tmp += 1
        answer.append(tmp)
        return
    for i in range(w):
        save = copy.deepcopy(board)
        destroy = []
        for j in range(h):
            if board[j][i] != 0:
                destroy.append([i, j, board[j][i]])
                break
        if len(destroy) != 0:
            boom(n, w, h, board, destroy)
        solve(n-1, w, h, board, answer)
        board = copy.deepcopy(save)

for t in range(int(input())):
    n, w, h = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(h)]
    answer = []
    solve(n, w, h, board, answer)
    answer.sort()
    print('#' + str(t+1), str(answer[0]))