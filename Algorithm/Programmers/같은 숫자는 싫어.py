def solution(arr):
    answer = []
    for n in arr:
        if len(answer) == 0:
            answer.append(n)
        else:
            if answer[-1] != n:
                answer.append(n)
    return answer