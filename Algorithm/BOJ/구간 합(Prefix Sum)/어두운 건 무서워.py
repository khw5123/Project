import sys
input = sys.stdin.readline

r, c, q = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(r)]
pSum = [[0]*(c+1) for _ in range(r+1)]
for i in range(r):
    for j in range(c):
        pSum[i+1][j+1] = pSum[i][j+1] + pSum[i+1][j] - pSum[i][j] + arr[i][j]
for _ in range(q):
    r1, c1, r2, c2 = map(int, input().split())
    answer = (pSum[r2][c2] - pSum[r2][c1-1] - pSum[r1-1][c2] + pSum[r1-1][c1-1]) // ((r2-r1+1)*(c2-c1+1))
    print(answer)