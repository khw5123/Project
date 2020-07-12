n, point = int(input()), -1
arr = list(map(int, input().split()))
for i in range(n-1, 0, -1):
    if arr[i-1] > arr[i]:
        point = i-1
        break
if point == -1:
    print(-1)
else:
    arr = arr[:point+1] + sorted(arr[point+1:], reverse=True)
    for i in range(point+1, n):
        if arr[point] > arr[i]:
            arr[point], arr[i] = arr[i], arr[point]
            break
    arr = arr[:point+1] + sorted(arr[point+1:], reverse=True)
    for v in arr:
        print(v, end=' ')
    print()