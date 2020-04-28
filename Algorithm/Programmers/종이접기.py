def solution(n):
    answer = [0]
    for i in range(1, n):
        answer.append(0)
        tmp = []
        for j in range(len(answer) - 2, -1, -1):
            tmp.append(1 if answer[j] == 0 else 0)
        answer += tmp
    return answer