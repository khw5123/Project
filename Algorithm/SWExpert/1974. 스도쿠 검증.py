for t in range(int(input())):
    board = [list(map(int, input().split())) for _ in range(9)]
    answer = 1
    for i in range(9):
        if sorted(board[i]) != [1,2,3,4,5,6,7,8,9]:
            answer = 0
    for i in range(9):
        tmp = []
        for j in range(9):
            tmp.append(board[j][i])
        if sorted(tmp) != [1,2,3,4,5,6,7,8,9]:
            answer = 0
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            tmp = []
            for a in range(i, i+3):
                for b in range(j, j+3):
                    tmp.append(board[a][b])
            if sorted(tmp) != [1,2,3,4,5,6,7,8,9]:
                answer = 0
    print('#' + str(t+1) + ' ' + str(answer))