for _ in range(10):
    n = int(input())
    board = [list(map(int, input().split())) for _ in range(100)]
    answer = 0
    for h in range(len(board)):
        answer = max(answer, sum(board[h]))
    for w in range(len(board[0])):
        save = 0
        for h in range(len(board)):
            save += board[h][w]
        answer = max(answer, save)
    save = 0
    for h in range(len(board)):
        save += board[h][h]
    answer = max(answer, save)
    save = 0
    for h in range(len(board)-1, -1, -1):
        save += board[h][len(board[0])-h-1]
    answer = max(answer, save)
    print('#' + str(n), str(answer))