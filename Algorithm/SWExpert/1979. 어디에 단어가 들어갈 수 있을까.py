for t in range(int(input())):
    n, k = map(int, input().split())
    board = [list(map(int, input().split())) for _ in range(n)]
    answer = list()
    for i in range(n):
        count = 0
        for j in range(n):
            if board[i][j] == 0:
                if count != 0:
                    answer.append(count)
                    count = 0
            elif board[i][j] == 1:
                count += 1
        if count != 0:
            answer.append(count)
    for i in range(n):
        count = 0
        for j in range(n):
            if board[j][i] == 0:
                if count != 0:
                    answer.append(count)
                    count = 0
            elif board[j][i] == 1:
                count += 1
        if count != 0:
            answer.append(count)
    print('#' + str(t+1) + ' ' + str(answer.count(k)))