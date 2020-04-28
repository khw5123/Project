def solution(weight):
    answer = 0
    weight.sort()
    for i in range(len(weight)):
        if answer + 1 < weight[i]:
            return answer + 1
        answer += weight[i]
    return answer + 1