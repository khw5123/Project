def solution(n, s):
    if n > s:
        return [-1]
    answer = [s // n] * n
    if sum(answer) != s:
        for i in range(s % n):
            answer[i] += 1
    answer.sort()
    return answer