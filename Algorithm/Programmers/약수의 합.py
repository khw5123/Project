import math

def solve(n):
    result = []
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            result.append(i)
            result.append(n//i)
    result = sorted(set(result))
    return result

def solution(n):
    answer = sum(solve(n))
    return answer