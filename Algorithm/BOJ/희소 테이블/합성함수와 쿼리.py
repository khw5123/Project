import sys
import math
input = sys.stdin.readline

m = int(input())
_next = [[0]*round(math.log2(500001)) for _ in range(m+1)]
f = list(map(int, input().split()))
for i in range(1, m+1):
    _next[i][0] = f[i-1]
for j in range(1, len(_next[0])):
    for i in range(1, m+1):
        _next[i][j] = _next[_next[i][j-1]][j-1]
for _ in range(int(input())):
    n, x = map(int, input().split())
    for i in range(len(_next[0])):
        if n | 1<<i == n:
            x = _next[x][i]
    print(x)