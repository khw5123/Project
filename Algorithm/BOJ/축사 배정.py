# 이분 매칭
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
        visit = [False]*(n+1)
        if dfs(nNode, n, m, match, nMatch, mMatch, visit):
            answer += 1
    # print(nMatch, mMatch)
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
# 네트워크 플로우(에드몬드 카프)
def solution(start, end):
    global v, capacity, flow, adj
    answer = 0
    while True:
        queue = [start] # 다음에 방문할 정점들
        path = [-1]*v # 방문 경로
        while queue:
            present = queue[0] # 현재 정점
            del queue[0]
            if present not in path:
                for _next in adj[present]:
                    # 흐를 수 있고, 다음 정점이 방문하지 않은 정점일 경우
                    if capacity[present][_next] - flow[present][_next] > 0 and path[_next] == -1:
                        queue.append(_next)
                        path[_next] = present
                        if _next == end: # 다음 방문할 정점이 도착지일 경우
                            break
        if path[end] == -1: # 가능한 모든 경로를 찾았을 경우
            break
        # 역방향
        flowRate = 9876543210 # 현재 경로에서의 최소 유량
        present = end
        while present != start:
            previous = path[present]
            flowRate = min(flowRate, capacity[previous][present] - flow[previous][present])
            present = path[present]
        present = end
        while present != start:
            previous = path[present]
            flow[previous][present] += flowRate
            flow[present][previous] -= flowRate # 음의 유량
            present = path[present]
        answer += flowRate
    return answer

n, m = map(int, input().split()) # 소의 수, 축사 수
v, _capacity = n+m+2, 1 # 정점 수, 모든 경로에서의 용량은 1로 고정
capacity = [[0]*v for _ in range(v)] # 용량
flow = [[0]*v for _ in range(v)] # 유량
adj = [[] for _ in range(v)] # 연결된 정점(source + 소 + 축사 + sink)
for _n in range(1, n+1): # source와 소 매칭
    adj[0].append(_n)
    adj[_n].append(0)
    capacity[0][_n] = _capacity
for _m in range(n+1, v-1): # 축사와 sink 매칭
    adj[_m].append(v-1)
    adj[v-1].append(_m)
    capacity[_m][v-1] = _capacity
for _n in range(1, n+1): # 소와 축사 매칭
    _input = list(map(int, input().split()))
    for _m in _input[1:]:
        adj[_n].append(_m+n)
        adj[_m+n].append(_n)
        capacity[_n][_m+n] = _capacity
print(solution(0, v-1))
'''