n, s = map(int, input().split())
arr = list(map(int, input().split()))
answer, _sum, end = 100000000, 0, 0
for start in range(len(arr)):
    while _sum < s and end < len(arr):
        _sum += arr[end]
        end += 1
    if _sum >= s:
        answer = min(answer, end-start)
    _sum -= arr[start]
print(0 if answer == 100000000 else answer)