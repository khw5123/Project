import bisect

def solution(A, B):
    answer = 0
    A.sort()
    B.sort()
    for n in A:
        idx = bisect.bisect(B, n)
        if idx != len(B):
            del B[bisect.bisect(B, n)]
            answer += 1
    return answer