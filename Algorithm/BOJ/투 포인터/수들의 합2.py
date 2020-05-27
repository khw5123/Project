n, m = map(int, input().split())
arr = list(map(int, input().split()))
answer, _sum, end = 0, 0, 0
for start in range(n):
    while _sum < m and end < n:
        _sum += arr[end]
        end += 1
    if _sum == m:
        answer += 1
    _sum -= arr[start]
print(answer)