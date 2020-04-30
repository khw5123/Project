for t in range(int(input())):
    answer = 0
    w, h, n = map(int, input().split())
    coordinate = []
    for _ in range(n):
        coordinate.append(list(map(int, input().split())))
    x, y = coordinate[0][0], coordinate[0][1]
    for i in range(1, len(coordinate)):
        if x == coordinate[i][0]:
            answer += abs(y - coordinate[i][1])
        elif y == coordinate[i][1]:
            answer += abs(x - coordinate[i][0])
        elif (x > coordinate[i][0] and y > coordinate[i][1]) or (x < coordinate[i][0] and y < coordinate[i][1]):
            answer += max(abs(x - coordinate[i][0]), abs(y - coordinate[i][1]))
        elif (x > coordinate[i][0] and y < coordinate[i][1]) or (x < coordinate[i][0] and y > coordinate[i][1]):
            answer += (abs(x - coordinate[i][0]) + abs(y - coordinate[i][1]))
        x, y = coordinate[i][0], coordinate[i][1]
    print('#' + str(t+1), str(answer))