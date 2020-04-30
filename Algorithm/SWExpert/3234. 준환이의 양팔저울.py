def solve(count, left, right, idx, weight, visit, dp):
    if left < right:
        return 0
    if count == len(weight):
        return 1
    if dp[idx] != -1:
        return dp[idx]
    ret = 0
    for i in range(len(weight)):
        if not visit[i]:
            visit[i] = True
            ret += solve(count+1, left+weight[i], right, idx | (1<<(i*2)), weight, visit, dp)
            ret += solve(count+1, left, right+weight[i], idx | ((1<<(i*2))<<1), weight, visit, dp)
            visit[i] = False
    dp[idx] = ret
    return ret

for t in range(int(input())):
    n = int(input())
    weight = list(map(int, input().split()))
    visit = [False]*n
    dp = [-1]*(((1<<(n*2))<<1)+1)
    answer = solve(0, 0, 0, 0, weight, visit, dp)
    print('#' + str(t+1), str(answer))