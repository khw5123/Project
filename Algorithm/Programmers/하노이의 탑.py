def solve(n, from_, by, to, answer):
    if n == 1:
        answer.append([from_, to])
    else:
        solve(n-1, from_, to, by, answer)
        answer.append([from_, to])
        solve(n-1, by, from_, to, answer)

def solution(n):
    answer = []
    solve(n, 1, 2, 3, answer)
    return answer