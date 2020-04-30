def check(board, target):
    result = True
    if (target[0]-1 >=0 and board[target[0]-1][target[1]] == '*') or (target[0]-1 >=0 and target[1]+1 < len(board[0]) and board[target[0]-1][target[1]+1] == '*') or (target[1]+1 < len(board[0]) and board[target[0]][target[1]+1] == '*') or (target[0]+1 < len(board) and target[1]+1 < len(board[0]) and board[target[0]+1][target[1]+1] == '*') or (target[0]+1 < len(board) and board[target[0]+1][target[1]] == '*') or (target[0]+1 < len(board) and target[1]-1 >= 0 and board[target[0]+1][target[1]-1] == '*') or (target[1]-1 >= 0 and board[target[0]][target[1]-1] == '*') or (target[0]-1 >=0 and target[1]-1 >= 0 and board[target[0]-1][target[1]-1] == '*'):
        result = False
    return result

def solve(board, target):
    board[target[0]][target[1]] = '@'
    if not check(board, target):
        return
    if target[0]-1 >=0 and board[target[0]-1][target[1]] == '.':
        solve(board, [target[0]-1, target[1]])
    if target[0]-1 >=0 and target[1]+1 < len(board[0]) and board[target[0]-1][target[1]+1] == '.':
        solve(board, [target[0]-1, target[1]+1])
    if target[1]+1 < len(board[0]) and board[target[0]][target[1]+1] == '.':
        solve(board, [target[0], target[1]+1])
    if target[0]+1 < len(board) and target[1]+1 < len(board[0]) and board[target[0]+1][target[1]+1] == '.':
        solve(board, [target[0]+1, target[1]+1])
    if target[0]+1 < len(board) and board[target[0]+1][target[1]] == '.':
        solve(board, [target[0]+1, target[1]])
    if target[0]+1 < len(board) and target[1]-1 >= 0 and board[target[0]+1][target[1]-1] == '.':
        solve(board, [target[0]+1, target[1]-1])
    if target[1]-1 >= 0 and board[target[0]][target[1]-1] == '.':
        solve(board, [target[0], target[1]-1])
    if target[0]-1 >=0 and target[1]-1 >= 0 and board[target[0]-1][target[1]-1] == '.':
        solve(board, [target[0]-1, target[1]-1])

for t in range(int(input())):
    n = int(input())
    answer = 0
    board = []
    for _ in range(n):
        board.append(list(map(str, input())))
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.':
                if check(board, [i, j]):
                    answer += 1
                    solve(board, [i, j])
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '.':
                answer += 1
    print('#' + str(t+1), str(answer))