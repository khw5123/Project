import sys
input = sys.stdin.readline

n, m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
pSum = [[0]*(n+1) for _ in range(n+1)]
for i in range(n):
    for j in range(n):
        pSum[i+1][j+1] = pSum[i][j+1] + pSum[i+1][j] - pSum[i][j] + arr[i][j]
for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    answer = pSum[x2][y2] - pSum[x2][y1-1] - pSum[x1-1][y2] + pSum[x1-1][y1-1]
    print(answer)