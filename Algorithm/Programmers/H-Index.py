def solution(citations):
    answer = 0
    citations.sort()
    for i in range(1, 10001):
        tmp = 0
        for j in range(len(citations)):
            if citations[j] >= i:
                tmp = len(citations) - j
                break
        if i <= tmp:
            answer = min(i, tmp)
    return answer