def case1(money):
    result = 0
    dp = [0]*len(money)
    dp[0], dp[1] = money[0], max(money[0], money[1])
    for i in range(2, len(money)-1):
        if dp[i-2]+money[i] > dp[i-1]:
            dp[i] = dp[i-2]+money[i]
        else:
            dp[i] = dp[i-1]
    result = dp[-2]
    return result

def case2(money):
    result = 0
    dp = [0]*len(money)
    dp[1] = money[1]
    for i in range(2, len(money)):
        if dp[i-2]+money[i] > dp[i-1]:
            dp[i] = dp[i-2]+money[i]
        else:
            dp[i] = dp[i-1]
    result = dp[-1]
    return result

def solution(money):
    answer = max(case1(money), case2(money))
    return answer