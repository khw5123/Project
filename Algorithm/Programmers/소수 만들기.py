from itertools import combinations

def func(num):
    arr = [i for i in range(num+1)]
    arr[0], arr[1] = -1, -1
    for i in range(2, len(arr)):
        if arr[i] != -1:
            for j in range(i+arr[i], len(arr), arr[i]):
                arr[j] = -1
    return 1 if arr[-1] != -1 else 0

def solution(nums):
    answer = 0
    for num in list(combinations(nums, 3)):
        answer += func(sum(num))
    return answer