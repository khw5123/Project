def demolish(n, board):
    for i in range(n+1):
        for j in range(n+1):
            if board[i][j][1] == 0: # 기둥일 경우
                # 바닥 위에 있지도 않고, 보의 한쪽 끝 부분 위에 있지도 않고, 다른 기둥 위에 있지도 않을 경우
                if i != 0 and (board[i][j][2] != 1 and board[i][j][3] != 1) and board[i][j][0] != 0:
                    return False
            if j > 0 and board[i][j-1][3] == 1 and board[i][j][2] == 1: # 왼쪽만 보일 경우
                # 양 쪽 끝 부분 모두 기둥 위에 있지 않고, 양쪽 끝 부분이 다른 보와 동시에 연결돼 있지 않을 경우
                if (board[i][j-1][0] != 0 and board[i][j][0] != 0) and (board[i][j-1][2] != 1 or board[i][j][3] != 1):
                    return False
            if j < n and board[i][j][3] == 1 and board[i][j+1][2] == 1: # 오른쪽만 보일 경우
                # 양 쪽 끝 부분 모두 기둥 위에 있지 않고, 양쪽 끝 부분이 다른 보와 동시에 연결돼 있지 않을 경우
                if (board[i][j][0] != 0 and board[i][j+1][0] != 0) and (board[i][j][2] != 1 or board[i][j+1][3] != 1):
                    return False
    return True

def build(n, x, y, a, board):
    result = False
    if a == 0: # 기둥 설치
        # 바닥 위에 있거나 보의 한쪽 끝 부분 위에 있거나 아래에 기둥이 있을 경우
        if y == 0 or (board[y][x][2] == 1 or board[y][x][3] == 1) or (y > 0 and board[y-1][x][1] == 0 and board[y][x][0] == 0):
            board[y][x][1], board[y+1][x][0] = 0, 0
            result = True
    else: # 보 설치
        # 한쪽 끝 부분이 기둥 위에 있거나 양쪽 끝 부분이 다른 보와 동시에 연결돼 있을 경우
        if ((y > 0 and board[y-1][x][1] == 0 and board[y][x][0] == 0) or (y > 0 and board[y-1][x+1][1] == 0 and board[y][x+1][0] == 0)) or \
            ((x > 0 and board[y][x-1][3] == 1 and board[y][x][2] == 1) and (x < n-1 and board[y][x+1][3] == 1 and board[y][x+2][2] == 1)):
            board[y][x][3], board[y][x+1][2] = 1, 1
            result = True
    return result

def solution(n, build_frame):
    answer = []
    board = [[[7, 7, 7, 7] for _ in range(n+1)] for _ in range(n+1)] # 아래 기둥, 위 기둥, 왼쪽 보, 오른쪽 보
    for x, y, a, b in build_frame:
        if b == 0: # 철거
            if a == 0: # 기둥
                board[y][x][1], board[y+1][x][0]  = 7, 7
            else: # 보
                board[y][x][3], board[y][x+1][2] = 7, 7
            if demolish(n, board): # 철거 가능
                for i in range(len(answer)):
                    if answer[i] == [x, y, a]:
                        del answer[i]
                        break
            else: # 철거 불가능
                if a == 0: # 기둥
                    board[y][x][1], board[y+1][x][0]  = 0, 0
                else: # 보
                    board[y][x][3], board[y][x+1][2] = 1, 1
        else: # 설치
            if build(n, x, y, a, board): # 설치 가능
                answer.append([x, y, a])
    answer.sort()
    return answer