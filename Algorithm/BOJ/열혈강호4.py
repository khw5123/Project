def dfs(nNode, n, m, match, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in match[nNode]:
        if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, m, match, nMatch, mMatch, visit):
            nMatch[nNode], mMatch[mNode] = mNode, nNode
            return True
    return False

def bipartiteMatch(n, m, k, match):
    answer, count = 0, 0
    nMatch, mMatch = [-1]*(n+1), [-1]*(m+1)
    while True:
        confirm = False
        for nNode in range(1, n+1):
            visit = [False]*(n+1)
            if dfs(nNode, n, m, match, nMatch, mMatch, visit):
                answer += 1
                confirm = True
                if count > 0:
                    k -= 1
                    if k == 0:
                        return answer
        if count > 0 and not confirm:
            break
        count += 1
    return answer

n, m, k = map(int, input().split())
match = [[] for _ in range(n+1)]
for n_ in range(1, n+1):
    tmp = list(map(int, input().split()))
    count, m_ = tmp[0], tmp[1:]
    for i in range(len(m_)):
        match[n_].append(m_[i])
print(bipartiteMatch(n, m, k, match))