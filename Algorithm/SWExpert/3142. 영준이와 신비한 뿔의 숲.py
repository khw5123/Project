for t in range(int(input())):
    n, m = map(int, input().split())
    arr = [[0]*(n+1) for _ in range(n+1)]
    print('#' + str(t+1), end=' ')
    for i in range(n+1):
        for j in range(n+1):
            arr[i][j] = i + j*2
            if arr[i][j] == n and i+j == m:
                print(i, j)