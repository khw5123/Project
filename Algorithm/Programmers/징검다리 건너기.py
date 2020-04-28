def solution(stones, k):
    answer = max(stones)
    jump = -1
    start = len(stones)-k
    for i in range(len(stones)-k):
        if stones[i] < stones[i+1]:
            start = i
            break
    for i in range(start, len(stones)-k+1):
        if jump > i:
            continue
        max_ = 0
        target = stones[i:i+k]
        for j in range(len(target)):
            if target[j] >= answer:
                max_ = target[j]
                jump = i+j+1
            max_ = max(max_, target[j])
        answer = min(answer, max_)
    return answer