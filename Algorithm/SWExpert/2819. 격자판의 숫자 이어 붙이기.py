def solve(visit, board, answer):
    if len(visit) == 7:
        tmp = ''
        for i in range(len(visit)):
            tmp += str(board[visit[i][1]][visit[i][0]])
        if tmp not in answer:
            answer.append(tmp)
        return
    for i in range(4):
        if i == 0:
            if visit[-1][1]-1 >= 0:
                visit.append([visit[-1][0], visit[-1][1]-1])
                solve(visit, board, answer)
                visit.pop()
        elif i == 1:
            if visit[-1][1]+1 < len(board):
                visit.append([visit[-1][0], visit[-1][1]+1])
                solve(visit, board, answer)
                visit.pop()
        elif i == 2:
            if visit[-1][0]-1 >= 0:
                visit.append([visit[-1][0]-1, visit[-1][1]])
                solve(visit, board, answer)
                visit.pop()
        else:
            if visit[-1][0]+1 < len(board[0]):
                visit.append([visit[-1][0]+1, visit[-1][1]])
                solve(visit, board, answer)
                visit.pop()

for t in range(int(input())):
    board = []
    answer = []
    for _ in range(4):
        board.append(list(map(int, input().split())))
    for i in range(len(board)):
        for j in range(len(board[0])):
            solve([[j, i]], board, answer)
    print('#' + str(t+1), str(len(answer)))