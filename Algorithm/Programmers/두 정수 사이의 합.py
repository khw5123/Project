def solution(a, b):
    answer = 0
    for i in range(b if a > b else a, (b if a < b else a) + 1):
        answer += i
    return answer