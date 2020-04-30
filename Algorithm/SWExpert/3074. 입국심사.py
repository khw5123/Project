def solve(n, times):
    left, right = 0, n*max(times)
    while left <= right:
        mid = (left + right) // 2
        tmp = 0
        for i in range(len(times)):
            tmp += (mid // times[i])
        if tmp >= n:
            right = mid - 1
        else:
            left = mid + 1
    return left

for t in range(int(input())):
    n, m = map(int, input().split())
    times = []
    for _ in range(n):
        times.append(int(input()))
    answer = solve(m, times)
    print('#' + str(t+1), str(answer))