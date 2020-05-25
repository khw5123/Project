def dfs(nNode, n, shark, nMatch, mMatch, visit):
    if visit[nNode]:
        return False
    visit[nNode] = True
    for mNode in range(nNode+1, n):
        if shark[nNode][0] >= shark[mNode][0] and shark[nNode][1] >= shark[mNode][1] and shark[nNode][2] >= shark[mNode][2]:
            if mMatch[mNode] == -1 or dfs(mMatch[mNode], n, shark, nMatch, mMatch, visit):
                nMatch[nNode], mMatch[mNode] = mNode, nNode
                return True
    return False

def bipartiteMatch(n, shark):
    answer = n
    nMatch, mMatch = [-1]*n, [-1]*n
    for nNode in range(n):
        for _ in range(2):
            visit = [False]*n
            if dfs(nNode, n, shark, nMatch, mMatch, visit):
                answer -= 1
    return answer

n = int(input())
shark = []
for _ in range(n):
    shark.append(list(map(int, input().split())))
shark.sort(reverse=True)
print(bipartiteMatch(n, shark))