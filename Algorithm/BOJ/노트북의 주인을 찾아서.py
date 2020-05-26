def dfs(nNode, n, m, match, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in match[nNode]:
        if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, m, match, nMatch, mMatch, visit):
            nMatch[nNode], mMatch[mNode] = mNode, nNode
            return True
    return False

def bipartiteMatch(n, m, match):
    answer = 0
    nMatch, mMatch = [-1]*(n+1), [-1]*(m+1)
    for nNode in range(1, n+1):
        visit = [False]*(n+1)
        if dfs(nNode, n, m, match, nMatch, mMatch, visit):
            answer += 1
    return answer

n, m = map(int, input().split())
match = [[] for _ in range(n+1)]
for _ in range(m):
    a, b = map(int, input().split())
    match[a].append(b)
print(bipartiteMatch(n, m+5000, match))