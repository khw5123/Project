import math

n, k, m = map(int, input().split())
_next = [[0]*round(math.log2(1000000001)) for _ in range(k+1)]
student = list(map(int, input().split()))
video = list(map(int, input().split()))
for i in range(1, k+1):
    _next[i][0] = video[i-1]
for j in range(1, len(_next[0])):
    for i in range(1, k+1):
        _next[i][j] = _next[_next[i][j-1]][j-1]
for x in student:
    for i in range(len(_next[0])):
        if m-1 | 1<<i == m-1:
            x = _next[x][i]
    print(x, end=' ')
print()