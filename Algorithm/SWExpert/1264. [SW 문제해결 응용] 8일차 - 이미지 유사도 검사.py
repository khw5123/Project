for t in range(int(input())):
    n = int(input())
    x, y = input(), input()
    dp = [[0]*(n+1) for i in range(n+1)]
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            if x[i-1] == y[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    answer = dp[n][n]/n*100
    print('#' + str(t+1), '%.2f' % answer)