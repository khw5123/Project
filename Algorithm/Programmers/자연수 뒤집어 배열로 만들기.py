def solution(n):
    answer = []
    for c in str(n):
        answer.insert(0, int(c))
    return answer