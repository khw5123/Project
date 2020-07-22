import sys
input = sys.stdin.readline

n, MAX = int(input()), 10000001
dist = [[MAX]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        if i == j:
            dist[i][j] = 0
for _ in range(int(input())):
    a, b, c = map(int, input().split())
    dist[a-1][b-1] = min(dist[a-1][b-1], c)
for k in range(n):
    for i in range(n):
        for j in range(n):
            dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j])
for i in range(n):
    for j in range(n):
        if dist[i][j] == MAX:
            dist[i][j] = 0
        print(dist[i][j], end=' ')
    print()