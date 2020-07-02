import sys
input = sys.stdin.readline

n = int(input())
arr = list(map(int, input().split()))
pSum = [0]*(n+1)
for i in range(n):
    pSum[i+1] = pSum[i] + arr[i]
for _ in range(int(input())):
    i, j = map(int, input().split())
    answer = pSum[j] - pSum[i-1]
    print(answer)