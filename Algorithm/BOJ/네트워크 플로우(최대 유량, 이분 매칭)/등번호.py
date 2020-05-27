import sys
sys.setrecursionlimit(10**6)

def dfs(nNode, n, match, nMatch, mMatch, visit, visitCount):
    if visit[nNode] == visitCount:
        return 0
    visit[nNode] = visitCount
    for mNode in match[nNode]:
        if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, match, nMatch, mMatch, visit, visitCount):
            nMatch[nNode], mMatch[mNode] = mNode, nNode
            return 1
    return 0

def bipartiteMatch(n, match):
    count, max_ = 0, pow(10, 6)+1
    nMatch, mMatch = [-1]*max_, [-1]*max_
    visit, visitCount = [0]*max_, 0
    for nNode in range(1, n+1):
        visitCount += 1
        count += dfs(nNode, n, match, nMatch, mMatch, visit, visitCount)
    return count, nMatch[1:n+1]

n = int(input())
match = [[0]*2 for _ in range(n+1)]
for node in range(1, n+1):
    match[node][0], match[node][1] = map(int, sys.stdin.readline().strip().split())
count, answer = bipartiteMatch(n, match)
if count == n:
    for v in answer:
        print(v)
else:
    print(-1)