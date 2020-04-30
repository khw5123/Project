for t in range(int(input())):
    n, m = map(int, input().split())
    farm = [[1]*n for _ in range(m)]
    answer = 0
    for i in range(m):
        for j in range(n):
            if farm[i][j] == 1:
                if j+2 < n:
                    farm[i][j+2] = 0
                if i+2 < m:
                    farm[i+2][j] = 0
    for i in range(m):
        for j in range(n):
            if farm[i][j] == 1:
                answer += 1
    print('#' + str(t+1), str(answer))