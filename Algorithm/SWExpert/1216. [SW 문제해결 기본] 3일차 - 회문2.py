def decide(arr):
    result = True
    for i in range(len(arr)//2):
        if arr[i] != arr[-(i+1)]:
            result = False
            break
    return result

for _ in range(10):
    n = int(input())
    board = [list(map(str, input())) for _ in range(100)]
    answer = 1
    for h in range(len(board)):
        for w in range(len(board[0])):
            length = answer + 1
            while w + length <= len(board[0]):
                if decide(board[h][w:w+length]):
                    answer = max(answer, length)
                length += 1
    for w in range(len(board[0])):
        for h in range(len(board)):
            length = answer + 1
            tmp = []
            for i in range(len(board)):
                tmp.append(board[i][w])
            while h + length <= len(tmp):
                if decide(tmp[h:h+length]):
                    answer = max(answer, length)
                length += 1
    print('#' + str(n), str(answer))