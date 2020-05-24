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
        for _ in range(2):
            visit = [False]*(n+1)
            if dfs(nNode, n, m, match, nMatch, mMatch, visit):
                answer += 1
    return answer

n, m = map(int, input().split())
match = [[] for _ in range(n+1)]
for n_ in range(1, n+1):
    tmp = list(map(int, input().split()))
    count, m_ = tmp[0], tmp[1:]
    for i in range(len(m_)):
        match[n_].append(m_[i])
print(bipartiteMatch(n, m, match))

'''
def dfs(nNode, n, m, match, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in range(1, m+1):
        if match[nNode][mNode]:
            if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, m, match, nMatch, mMatch, visit):
                nMatch[nNode], mMatch[mNode] = mNode, nNode
                return True
    return False

def bipartiteMatch(n, m, match):
    answer = 0
    nMatch, mMatch = [-1]*(n+1), [-1]*(m+1)
    for nNode in range(1, n+1):
        for _ in range(2):
            visit = [False]*(n+1)
            if dfs(nNode, n, m, match, nMatch, mMatch, visit):
                answer += 1
    return answer

n, m = map(int, input().split())
match = [[0]*(m+1) for _ in range(n+1)]
for n_ in range(1, n+1):
    tmp = list(map(int, input().split()))
    count, m_ = tmp[0], tmp[1:]
    for i in range(len(m_)):
        match[n_][m_[i]] = 1
print(bipartiteMatch(n, m, match))
'''