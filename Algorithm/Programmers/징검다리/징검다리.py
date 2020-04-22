def solution(distance, rocks, n):
    answer = 0
    left, right = 0, distance
    rocks.sort()
    rocks.append(distance)
    while left <= right:
        prev = 0
        min_ = 1000000001
        remove = 0
        mid = (left + right) // 2
        for i in range(len(rocks)):
            if rocks[i] - prev < mid:
                remove += 1
            else:
                min_ = min(min_, rocks[i] - prev)
                prev = rocks[i]
        if remove > n:
            right = mid - 1
        else:
            answer = min_
            left = mid + 1
    return answer