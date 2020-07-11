MAX = 10000
dp = [[0]*3 for _ in range(MAX+1)]
dp[1][0] = 1 # 1
dp[2][0], dp[2][1] = 1, 1 # 2, 1+1
dp[3][0], dp[3][1], dp[3][2] = 1, 1, 1 # 3, 2+1, 1+1+1
for i in range(4, MAX+1):
    dp[i][0] = 1
    dp[i][1] = dp[i-2][0] + dp[i-2][1]
    dp[i][2] = dp[i-3][0] + dp[i-3][1] + dp[i-3][2]
for _ in range(int(input())):
    n = int(input())
    print(sum(dp[n]))