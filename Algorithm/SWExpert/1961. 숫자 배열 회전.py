import copy

for t in range(int(input())):
    n = int(input())
    answer = [['']*3 for _ in range(n)]
    board = [list(map(int, input().split())) for _ in range(n)]
    change = [[0]*n for _ in range(n)]
    for c in range(3):
        for i in range(n):
            for j in range(n-1, -1, -1):
                change[i][n-j-1] = board[j][i]
        board = copy.deepcopy(change)
        for i in range(n):
            tmp = ''
            for j in range(n):
                tmp += str(board[i][j])
            answer[i][c] = tmp
    print('#' + str(t+1))
    for i in range(n):
        for j in range(3):
            print(answer[i][j], end=' ')
        print()