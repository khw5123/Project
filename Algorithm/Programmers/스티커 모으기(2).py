def case1(sticker):
    result = 0
    dp = [0]*len(sticker)
    dp[0], dp[1] = sticker[0], max(sticker[0], sticker[1])
    for i in range(2, len(sticker)-1):
        if dp[i-2]+sticker[i] > dp[i-1]:
            dp[i] = dp[i-2]+sticker[i]
        else:
            dp[i] = dp[i-1]
    result = dp[-2]
    return result

def case2(sticker):
    result = 0
    dp = [0]*len(sticker)
    dp[1] = sticker[1]
    for i in range(2, len(sticker)):
        if dp[i-2]+sticker[i] > dp[i-1]:
            dp[i] = dp[i-2]+sticker[i]
        else:
            dp[i] = dp[i-1]
    result = dp[-1]
    return result

def solution(sticker):
    if len(sticker) == 1:
        answer = sticker[0]
    else:
        answer = max(case1(sticker), case2(sticker))
    return answer