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

for _ in range(int(input())):
    n, m = map(int, input().split())
    n, m = m, n # 편의상 n을 학생수로 m을 책 개수로 설정
    match = [[] for _ in range(n+1)]
    for _n in range(1, n+1):
        a, b = map(int, input().split())
        for i in range(a, b+1):
            match[_n].append(i)
    print(bipartiteMatch(n, m, match))