def decide(arr):
    result = True
    for i in range(len(arr)//2):
        if arr[i] != arr[-(i+1)]:
            result = False
            break
    return result

for t in range(10):
    length = int(input())
    board = [list(map(str, input())) for _ in range(8)]
    answer = 0
    for h in range(len(board)):
        for w in range(len(board[0])-length+1):
            if decide(board[h][w:w+length]):
                answer += 1
    for w in range(len(board[0])):
        for h in range(len(board)-length+1):
            tmp = []
            for i in range(h, h+length):
                tmp.append(board[i][w])
            if decide(tmp):
                answer += 1
    print('#' + str(t+1), str(answer))