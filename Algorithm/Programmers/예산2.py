def solution(d, budget):
    answer = 0
    d.sort()
    if sum(d) <= budget:
        answer = len(d)
    else:
        tmp = 0
        for i in range(len(d)):
            tmp += d[i]
            print(tmp)
            if tmp > budget:
                answer = i
                break
    return answer