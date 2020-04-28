def solution(n):
    answer = 0
    arr = [i for i in range(2, n+1)]
    for i in range(len(arr)):
        if arr[i] != -1:
            for j in range(i+arr[i], len(arr), arr[i]):
                arr[j] = -1
    answer = len([i for i in arr if i != -1])
    return answer