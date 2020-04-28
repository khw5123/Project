def solution(n):
    answer = ''.join(['박' if i % 2 == 0 else '수' for i in range(1, n+1)])
    return answer