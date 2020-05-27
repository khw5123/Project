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
    nMatch, mMatch = [-1]*n, [-1]*m
    for nNode in range(n):
        if match[nNode]: # 기준 자리에서 컨닝 가능한 자리가 있을 경우
            visit = [False]*n
            if dfs(nNode, n, m, match, nMatch, mMatch, visit):
                answer += 1
    return answer

for _ in range(int(input())):
    h, w = map(int, input().split())
    classroom = [list(map(str, input())) for _ in range(h)]
    n, m = 50, 50 # 기준 자리(짝수 번째 열), 기준 자리에서 컨닝 가능한 자리(홀수 번째 열) 개수 초기화
    match = [[] for _ in range(n)]
    node = [[0]*w for _ in range(h)] # 자리(정점) 이름
    nCount, mCount = 0, 0
    answer = h*w # 모든 자리 수를 정답으로 초기화
    for i in range(h):
        for j in range(0, w, 2): # 기준 자리 열 개수만큼 반복
            node[i][j] = nCount # 기준 자리 이름 설정
            nCount += 1
            if classroom[i][j] == 'x':
                answer -= 1 # 모든 자리 수에서 부숴진 자리 수 차감
    for i in range(h):
        for j in range(1, w, 2): # 기준 자리에서 컨닝 가능한 자리 열 개수만큼 반복
            node[i][j] = mCount # 기준 자리에서 컨닝 가능한 자리 이름 설정
            mCount += 1
            if classroom[i][j] == 'x':
                answer -= 1
    for i in range(h):
        for j in range(0, w, 2): # 기준 자리 열 개수만큼 반복
            if classroom[i][j] != 'x': # 부숴진 자리가 아닐 경우
                for dx, dy in [[-1, -1], [-1, 0], [-1, 1], [1, -1], [1, 0], [1, 1]]:
                    x, y = j+dx, i+dy
                    if 0 <= x and x < w and 0 <= y and y < h:
                        if classroom[y][x] != 'x':
                            match[node[i][j]].append(node[y][x]) # 기준 자리와 기준 자리에서 컨닝 가능한 자리 매칭
    # 최대 유량은 서로 컨닝 가능한 자리들의 최대 개수이므로 해당 개수만큼 차감
    answer -= bipartiteMatch(n, m, match)
    print(answer)