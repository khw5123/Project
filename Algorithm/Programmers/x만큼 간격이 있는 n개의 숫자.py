def solution(x, n):
    answer = [x]
    for _ in range(1, n):
        answer.append(answer[-1] + x)
    return answer