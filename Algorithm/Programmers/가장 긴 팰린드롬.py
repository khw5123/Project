def solution(s):
    answer = 1
    for i in range(len(s), 1, -1):
        for j in range(len(s)-i+1):
            try:
                tmp = 0
                for k in range(i//2):
                    if s[j+k] == s[j+i-k-1] and j+k != j+i-k-1:
                        tmp += 1
                    else:
                        tmp = 0
                        break
                if i % 2 == 0:
                    answer = max(answer, tmp*2)
                else:
                    answer = max(answer, tmp*2 + 1)
            except:
                pass
        if answer == i:
            break
    return answer