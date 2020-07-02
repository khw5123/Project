import sys
input = sys.stdin.readline

s = input()
pSumDict = dict()
for _ in range(int(input())):
    c, l, r = map(str, input().split())
    l, r = int(l), int(r)
    if c not in pSumDict:
        arr = [1 if char == c else 0 for char in s]
        pSum = [0]*(len(s)+1)
        for i in range(len(s)):
            pSum[i+1] = pSum[i] + arr[i]
        pSumDict[c] = pSum
    answer = pSumDict[c][r+1] - pSumDict[c][l]
    print(answer)