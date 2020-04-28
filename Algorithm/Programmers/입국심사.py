def solution(n, times):
    answer = 0
    left, right = 0, n * max(times)
    while left <= right:
        mid = (left + right) // 2
        tmp = 0
        for i in range(len(times)):
            tmp += (mid // times[i])
        if tmp >= n:
            right = mid - 1
        else:
            left = mid + 1
    answer = left
    return answer