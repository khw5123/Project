import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
arr = list(map(int, input().split()))
boundary, count = dict(), list()
for _ in range(m):
    a, b = map(int, input().split())
    boundary[(a-1, b-1)] = 1
if m == 0 or m == 1:
    print('YES')
else:
    _min = 1000001
    for i in range(n):
        _min = min(_min, arr[i])
        if (i, i+1) in boundary:
            count.append(_min)
            _min = arr[i+1]
    if (n-1, 0) in boundary:
        count.append(_min)
    else:
        count[0] = min(count[0], _min)
    if sum(count) <= k:
        print('YES')
    else:
        print('NO')