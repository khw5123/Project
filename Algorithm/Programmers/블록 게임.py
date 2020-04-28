def fill(board):
    for x in range(len(board[0])):
        for y in range(len(board)):
            if board[y][x] == 0:
                board[y][x] = -1
            else:
                break

def empty(board):
    result = 0
    for y in range(len(board)-(2-1)):
        for x in range(len(board[0])-(3-1)):
            tmp = dict()
            for i in range(y, y+2):
                for j in range(x, x+3):
                    if board[i][j] not in tmp:
                        tmp[board[i][j]] = 1
                    else:
                        tmp[board[i][j]] += 1
            if len(tmp) == 2:
                confirm = 0
                for k, v in tmp.items():
                    if k == -1 and v == 2:
                        confirm += 1
                    elif (k != -1 and k != 0) and v == 4:
                        confirm += 1
                if confirm == 2:
                    for i in range(y, y+2):
                        for j in range(x, x+3):
                            board[i][j] = 0
                    result += 1
    for y in range(len(board)-(3-1)):
        for x in range(len(board[0])-(2-1)):
            tmp = dict()
            for i in range(y, y+3):
                for j in range(x, x+2):
                    if board[i][j] not in tmp:
                        tmp[board[i][j]] = 1
                    else:
                        tmp[board[i][j]] += 1
            if len(tmp) == 2:
                confirm = 0
                for k, v in tmp.items():
                    if k == -1 and v == 2:
                        confirm += 1
                    elif (k != -1 and k != 0) and v == 4:
                        confirm += 1
                if confirm == 2:
                    for i in range(y, y+3):
                        for j in range(x, x+2):
                            board[i][j] = 0
                    result += 1
    return result

def restore(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == -1:
                board[y][x] = 0

def solution(board):
    answer = 0
    while True:
        fill(board)
        result = empty(board)
        if result:
            answer += result
            restore(board)
        else:
            break
    return answer