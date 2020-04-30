def solve(flag):
    global n, forward, dp
    if flag == (1<<n)-1:
        return 1
    if dp[flag] != -1:
        return dp[flag]
    dp[flag] = 0
    for i in range(n):
        if flag & 1<<i == 0 and flag & forward[i] == forward[i]:
            dp[flag] += solve(flag | 1<<i)
    return dp[flag]

for t in range(int(input())):
    n, m = map(int, input().split())
    forward = [0]*16
    dp = [-1]*(1<<n)
    for i in range(m):
        x, y = map(int, input().split())
        forward[y-1] |= 1<<(x-1)
    answer = solve(0)
    print('#' + str(t+1), str(answer))