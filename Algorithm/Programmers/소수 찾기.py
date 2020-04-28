import math
from itertools import permutations

def func(n):
    if n <= 1:
        return False
    if n > 2 and n % 2 == 0:
        return False
    return all(n % i for i in range(3, int(math.sqrt(n))+1, 2))

def solution(numbers):
    answer = 0
    save = list()
    for i in range(1, len(numbers)+1):
        save += list(permutations(numbers, i))
    tmp = list()
    for case in set(save):
        n = int(''.join(list(case)))
        if n not in tmp:
            if func(n):
                answer += 1
            tmp.append(n)
    return answer