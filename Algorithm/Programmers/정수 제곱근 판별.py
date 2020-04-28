import math

def solution(n):
    answer = 0
    if math.sqrt(n) - int(math.sqrt(n)) != 0:
        answer = -1
    else:
        answer = pow(math.sqrt(n) + 1, 2)
    return answer