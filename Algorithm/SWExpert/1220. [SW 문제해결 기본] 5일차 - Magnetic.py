for t in range(10):
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    for i in range(n):
        tmp = False
        for j in range(n):
            if board[j][i] == 1:
                tmp = True
            if tmp == True and board[j][i] == 2:
                answer += 1
                tmp = False
    print('#' + str(t+1), str(answer))