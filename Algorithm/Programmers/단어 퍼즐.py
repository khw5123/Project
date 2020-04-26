def solution(strs, t):
    answer = 0
    dp, di = [0]*len(t), dict()
    for i in range(len(strs)):
        if strs[i][-1] in di:
            di[strs[i][-1]].append(strs[i])
        else:
            di[strs[i][-1]] = [strs[i]]
    for i in range(len(t)):
        if t[i] in di:
            save = []
            for s in di[t[i]]:
                if len(s) <= i+1:
                    if s == t[i-len(s)+1:i+1]:
                        save.append(s)
            if len(save) == 0:
                dp[i] = len(t)+1
                continue
            for s in save:
                if len(s)-1 == i:
                    dp[i] = 1
                else:
                    if dp[i] != 0:
                        if dp[i] > dp[i-len(s)]+1:
                            dp[i] = dp[i-len(s)]+1
                    else:
                        dp[i] = dp[i-len(s)]+1
        else:
            dp[i] += len(t)+1
    answer = dp[-1]
    if answer > len(t):
        answer = -1
    return answer