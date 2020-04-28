def solution(clothes):
    answer = 1
    di = dict()
    for i in range(len(clothes)):
        if clothes[i][1] not in di:
            di[clothes[i][1]] = 1
        else:
            di[clothes[i][1]] += 1
    for k, v in di.items():
        answer *= v + 1
    answer -= 1
    return answer