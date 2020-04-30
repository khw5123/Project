for t in range(int(input())):
    n, k = map(int, input().split())
    arr = [[0]*(k+1) for _ in range(n+1)]
    for i in range(1, n+1):
        v, c = map(int, input().split())
        for j in range(1, k+1):
            if v <= j:
                if c + arr[i-1][j-v] > arr[i-1][j]:
                    arr[i][j] = c + arr[i-1][j-v]
                else:
                    arr[i][j] = arr[i-1][j]
            else:
                arr[i][j] = arr[i-1][j]
    print('#' + str(t+1), str(arr[n][k]))