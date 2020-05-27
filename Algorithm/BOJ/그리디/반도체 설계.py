def solution(n, port):
    dp = [1]*n
    for i in range(1, n):
        for j in range(i):
            if port[i] > port[j]:
                dp[i] = max(dp[i], dp[j]+1)
    return max(dp)

n = int(input())
port = list(map(int, input().split()))
print(solution(n, port))