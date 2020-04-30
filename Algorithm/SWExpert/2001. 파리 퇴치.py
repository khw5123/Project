for t in range(int(input())):
    n, m = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    answer = 0
    for i in range(n - m + 1):
        for j in range(n - m + 1):
            tmp = 0
            for a in range(i, i + m):
                for b in range(j, j + m):
                    tmp += board[a][b]
            answer = max(answer, tmp)
    print('#' + str(t+1) + ' ' + str(answer))