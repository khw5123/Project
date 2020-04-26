import math

def solution(land, P, Q):
    answer = math.inf
    li = []
    for i in range(len(land)):
        for j in range(len(land[0])):
            li.append(land[i][j])
    li.sort()
    sum_, total = 0, sum(li)
    for i in range(len(li)):
        p = P*((li[i]*(i))-sum_)
        sum_ += li[i]
        q = Q*(total-sum_-(li[i]*(len(li)-(i+1))))
        answer = min(answer, p+q)
    return answer