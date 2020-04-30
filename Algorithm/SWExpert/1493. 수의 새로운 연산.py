li = [[0]*300 for _ in range(300)]
num = 1
for i in range(1, len(li)):
    for j in range(i):
        li[i-j][j+1] = num
        num += 1

for t in range(int(input())):
    p, q = map(int, input().split())
    coordinate = [0, 0]
    for i in range(len(li)):
        for j in range(len(li)):
            if li[i][j] == p:
                coordinate[0] += j
                coordinate[1] += i
            if li[i][j] == q:
                coordinate[0] += j
                coordinate[1] += i
    print('#' + str(t+1), str(li[coordinate[1]][coordinate[0]]))