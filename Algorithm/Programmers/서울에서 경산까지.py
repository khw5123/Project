def solution(K, travel):
    answer = 0
    dp = [[0]*(K+1) for _ in range(len(travel)+1)]
    dp[0][travel[0][0]], dp[0][travel[0][2]] = travel[0][1], travel[0][3]
    for i in range(1, len(travel)):
        for j in range(K+1):
            if dp[i-1][j] != 0:
                if j + travel[i][0] <= K:
                    dp[i][j+travel[i][0]] = max(dp[i][j+travel[i][0]], dp[i-1][j] + travel[i][1])
                    answer = max(answer, dp[i][j+travel[i][0]])
                if j + travel[i][2] <= K:
                    dp[i][j+travel[i][2]] = max(dp[i][j+travel[i][2]], dp[i-1][j] + travel[i][3])
                    answer = max(answer, dp[i][j+travel[i][2]])
    return answer